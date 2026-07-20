from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from employees.models import Employee
from accounts.models import User
from attendance.models import Attendance
from documents.models import EmployeeDocument
from leave_management.models import LeaveBalance
from complaint.models import Complaint,ComplaintTimeline
from .serializers import CreateEmployeeSerializer,EmployeeListSerializer,EmployeeUpdateSerializer,HRDocumentSerializer,LeaveRequest,HRLeaveSerializer,HRComplaintSerializer,ComplaintTimelineSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import calendar

from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
# Create your views here.
# hrdashboard summary api

class HRDashboardView(APIView):
    def get(self,request):
        total_employees = Employee.objects.count()

        active_employees = Attendance.objects.filter(
            status="Checked In"
        ).count()

        departments = (
            Employee.objects.values("department")
            .distinct()
            .count()
        )

        recent_joiners = Employee.objects.order_by("-date_of_joining")[:5]

        return Response({
            "total_employees": total_employees,
            "active_employees": active_employees,
            "departments": departments,
            "recent_joiners":[
                {
                    "name": emp.user.first_name,
                    "department": emp.department,
                }
                for emp in recent_joiners
            ]
        })

#  for manage employees table.

class EmployeeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        employees = Employee.objects.all()

        data = []

        for emp in employees:
            data.append({
                "id": emp.employee_id,
                "name": f"{emp.user.first_name} {emp.user.last_name}",
                "email": emp.user.email,
                "department": emp.department,
                "designation": emp.designation,
                "joiningDate": emp.date_of_joining,
            })

        return Response(data)
    
class CreateEmployeeView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):
        
        serializer = CreateEmployeeSerializer(data=request.data)
        
        if serializer.is_valid():
            employee = serializer.save()

            return Response(
                {
                    "message":"Employee created successfully."
                },
                status=201
            )
        return Response(
            serializer.errors,
            status=400
        )
        
class EmployeeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        employees = Employee.objects.select_related("user").all()

        serializer = EmployeeListSerializer(employees,many=True)

        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_employees_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    
    response["Content-Disposition"] = 'inline; filename="employees.pdf"'

    doc = SimpleDocTemplate(response)

    elements = []

    data = [[
        "Employee ID",
        "Name",
        "Email",
        "Department",
        "Designation",
        "Joining Date",
    ]]

    employees = Employee.objects.all()

    for employee in employees:
        
        latest_attendance = (
            Attendance.objects
            .filter(user=employee.user)
            .order_by("-attendance_date","-check_in")
            .first()
        )



        data.append([
            employee.employee_id,
            f"{employee.user.first_name} {employee.user.last_name}",
            employee.user.email,
            employee.department,
            employee.designation,
            employee.date_of_joining.strftime("%d-%m-%Y"),
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#36136E")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,1),(-1,-1),colors.beige),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BOTTOMPADDING",(0,0),(-1,0),10),
        ("ALIGN",(0,0),(-1,-1),"CENTER")
    ]))

    elements.append(table)

    doc.build(elements)

    return response

class EmployeeDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request,employee_id):

        try:
            employee = Employee.objects.get(employee_id=employee_id)

        except Employee.DoesNotExist:
            return Response(
                {"detail":"Employee not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = EmployeeUpdateSerializer(employee)

        return Response(serializer.data)
    
    def patch(self,request,employee_id):

        employee = Employee.objects.get(employee_id=employee_id)

        serializer = EmployeeUpdateSerializer(
            employee,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Employee updated successfully."
            })
        
        return Response(serializer.errors,status=400)
    
    def delete(self,request,employee_id):
        try:
            employee = Employee.objects.get(employee_id=employee_id)

        except Employee.DoesNotExist:
            return Response(
                {"message": "Employee not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        print("Before delete:",Employee.objects.filter(employee_id=employee_id).exists())

        employee.user.delete()

        print("After delete:",Employee.objects.filter(employee_id=employee_id).exists())

        return Response(
            {"message": "Employee deleted successfully."},
            status=status.HTTP_200_OK,
        )
    

# FOR VIEWING EMPLOYEE UPLOADED DOCUMENTS IN HR DASHBOARD

class HRDocumentListView(APIView):

    def get(self,request):

        documents = EmployeeDocument.objects.select_related("user","user__employee").all()
        serializer = HRDocumentSerializer(documents,many=True,context={"request":request})

        return Response(serializer.data)

class VerifyDocumentView(APIView):

    def patch(self,request,pk):

        document = EmployeeDocument.objects.get(pk=pk)

        document.status = "Verified"
        document.save()

        return Response({
            "message":"Document verified successfully."
        })


# FOR LEAVE REQUEST APPROVAL,REJECTION

class HRLeaveListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):

        leaves = LeaveRequest.objects.select_related(
            "user",
            "user__employee"
        ).order_by("-applied_on")

        serializer = HRLeaveSerializer(
            leaves,
            many=True
        )

        summary = {
            "total": leaves.count(),
            "pending": leaves.filter(status="Pending").count(),
            "approved": leaves.filter(status="Approved").count(),
            "rejected": leaves.filter(status="Rejected").count(),
        }

        return Response(
            {
                "summary":summary,
                "leave_requests": serializer.data,
                "activities": []
            }
        )
    

class HRLeaveDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):

        leave = get_object_or_404(
            LeaveRequest.objects.select_related(
                "user",
                "user__employee"
            ),
            pk=pk
        )

        serializer = HRLeaveSerializer(
            leave,
            context={"request":request}
        )
        return Response(serializer.data)


# (leave approval) 

class ApproveLeaveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self,request,pk):
        leave = get_object_or_404(LeaveRequest,pk=pk)

        if leave.status != "Pending":
            return Response(
                {"message": "Leave already processed."},
                status=400
            )
        
        balance = LeaveBalance.objects.get(user=leave.user)

        days = leave.total_days()

        if leave.leave_type == "Casual Leave":

            if balance.casual_leave < days :
                return Response(
                    {"message":"Insufficient casual leave balance"},
                    status=400
                )
            
            balance.casual_leave -= days

        elif leave.leave_type == "Sick Leave":
            
            if balance.sick_leave < days:
                return Response(
                    {"message":"Insufficient sick leave balance."},
                    status=400
                )
            balance.privilege_leave -= days

        balance.save()

        leave.status = "Approved"
        leave.save()

        return Response({
            "message":"Leave approved succesfully."
        })
    
class RejectLeaveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self,request,pk):

        leave = get_object_or_404(
            LeaveRequest,
            pk=pk
        )

        if leave.status != "Pending":
            return Response(
                {"message":"Leave already processed."},
                status=400
            )
        
        leave.status = "Rejected"
        leave.save()

        return Response({
            "message":"Leave rejected succesfully."
        })
    
    # FOR COMPLAINT

class HRComplaintListAPIView(APIView):
        
        permission_classes=[IsAuthenticated]

        def get(self,request):

            complaints = Complaint.objects.select_related(
                "user",
                "user__employee"
            ).order_by("created_at")

            serializer = HRComplaintSerializer(complaints,many=True)

            summary = {
                "total": complaints.count(),
                "pending": complaints.filter(status="Pending").count(),
                "review": complaints.filter(status="In Review").count(),
                "resolved": complaints.filter(status="Resolved").count(),
                "escalated": complaints.filter(status="Escalated").count(),
            }

            timeline = (
                ComplaintTimeline.objects
                .select_related("complaint","complaint__user")
                .order_by("-created_at")[:10]
            )

            activities = []

            for item in timeline:
                activities.append({
                    "id":item.id,
                    "complaint":f"CMP-{item.complaint.id:04d}",
                    "employee_name":f"{item.complaint.user.first_name} {item.complaint.user.last_name}",
                    "action": item.step,
                    "time":item.created_at,
                })

            return Response({
                "summary":summary,
                "complaints":serializer.data,
                "activities":activities,
            })
        

# COMPLAINT DETAIL API

class HRComplaintDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):

        complaint = get_object_or_404(
            Complaint.objects.select_related(
                "user",
                "user__employee"
            ),
            pk=pk
        )

        serializer = HRComplaintSerializer(
            complaint,
            context={"request":request}
        )

        serializer = HRComplaintSerializer(
            complaint,
            context={"request":request}
        )

        return Response(serializer.data)
    
class UpdateComplaintStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self,request,pk):

        complaint= get_object_or_404(
            Complaint,
            pk=pk
        )

        status = request.data.get("status")

        valid_status = [
            "Pending",
            "In Review",
            "Escalated",
            "Resolved"
        ]

        if status not in valid_status:
            return Response(
                {"message":"Invalid Status"},
                status=400
            )
        
        complaint.status = status
        complaint.save()

        ComplaintTimeline.objects.create(
            complaint=complaint,
            step=f"Status updated to {complaint.status}"
        )

        return Response({
            "message":"Complaint updated succesfully."
        })
    

class ComplaintTimelineAPIView(ListAPIView):

    serializer_class = ComplaintTimelineSerializer

    def get_queryset(self):
        return (
            ComplaintTimeline.objects
            .select_related("complaint")
            .order_by("-created_at")[:3]
        )
    
class AttendanceAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        today = timezone.now().date()

        total_employees = Employee.objects.count()

        today_records = Attendance.objects.filter(attendance_date=today)

        present = today_records.filter(status__in=["Present","Late"]).count()

        attendance_rate = 0
        if total_employees > 0:
            attendance_rate =round((present/total_employees) *100,2)

            total_hours = 0
            worked_count = 0

            for record in today_records:
                if record.work_hours:
                    total_hours += (record.work_hours.total_seconds() / 3600)
                    worked_count += 1
            average_hours = 0 
            if worked_count > 0:
                 average_hours = round(
                     total_hours / worked_count,2
                 )
            
            check_in = today_records.filter(
                check_in__isnull=False,
                check_out__isnull=True
            ).count()

            return Response({
                "attendance_rate": attendance_rate,
                "average_working_hours": average_hours,
                "check_in_employees": check_in
            })
        
class HRAttendanceSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        today = timezone.now().date()

        total_employees = Employee.objects.count()

        today_records = Attendance.objects.filter(attendance_date=today)

        present_today = today_records.filter(status__in=["Present","Late"]).count()

        late_today = today_records.filter(status="Late").count()

        absent_today = max(total_employees - present_today,0)

        return Response({
            "total_employees": total_employees,
            "present_today":present_today,
            "late_today":late_today,
            "absent_today":absent_today,
        })
    
class HRAttendanceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        today = timezone.now().date()

        employees = Employee.objects.select_related("user")
        
        records = []

        for employee in employees:

            attendance = Attendance.objects.filter(user=employee.user,attendance_date=today).first()

            if attendance:

                if attendance.check_in:
                    check_in = attendance.check_in.strftime("%I:%M %p")
                else:
                    check_in= "--"

                if attendance.check_out:
                    check_out = attendance.check_out.strftime("%I:%M %p")
                else:
                    check_out = "--"

                if attendance.work_hours:
                    hours = round(attendance.work_hours.total_seconds() / 3600,2)
                    hours_worked = f"{hours}h"
                else:
                    hours_worked = "--"

                punctuality = (
                    "Late"
                    if attendance.status == "Late"
                    else "On Time"
                )

                status = attendance.status

            else:
                check_in = "--"
                check_out = "--"
                hours_worked = "--"
                status = "Absent"
                punctuality = "Absent"

            records.append({
                "id": employee.employee_id,
                "name": employee.user.get_full_name(),
                "department": employee.department,
                "checkIn": check_in,
                "checkOut": check_out,
                "hoursWorked": hours_worked,
                "status": status,
                "punctuality": punctuality,
            })

        return Response(records)
    
class HRWeeklyAttendanceGraphView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        today = timezone.now().date()

        # monday of current week
        start_date = today - timedelta(days=today.weekday())

        data =[]

        for i in range(6):
            current_date = start_date +timedelta(days=i)

            on_time = Attendance.objects.filter(
                attendance_date=current_date,
                status="Present"
            ).count()

            late = Attendance.objects.filter(attendance_date=current_date,status="Late").count()

            data.append({
                "day": current_date.strftime("%a"),
                "date": current_date.strftime("%d-%m"),
                "on_time":on_time,
                "late":late,
            })
        return Response(data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hr_monthly_attendance_pdf(request):
    employee_id = request.GET.get("employee_id")
    month = int(request.GET.get("month"))
    year = int(request.GET.get("year"))

    employee = Employee.objects.filter(employee_id=employee_id).first()

    if not employee:
        return Response(
            {
                "message":"Employee ID does not exist."
            },
            status=404
        )

    attendance = Attendance.objects.filter(
        user=employee.user,
        attendance_date__month=month,
        attendance_date__year=year
    ).order_by("attendance_date")

    response = HttpResponse(content_type="application/pdf")
    response["content-Disposition"]= (
     f'inline; filename="{employee.employee_id}_attendance.pdf'
    )
    doc = SimpleDocTemplate(response)

    elements = []
    styles = getSampleStyleSheet()

    elements.append(
        Paragraph("<b>Monthly Attendance Report</b>",styles["Heading1"])
    )

    elements.append(
        Paragraph(
            f"Employee ID: {employee.employee_id}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Department:{employee.department}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Month:{month}/{year}",
            styles["Normal"]
        )
    )

    elements.append(Paragraph("<br/>",styles["Normal"]))

    data = [[
        "Date",
        "Day",
        "Check In",
        "Check Out",
        "Hours",
        "Status"
    ]]

    present = 0
    late = 0 
    total_hours = 0

    for record in attendance:
        hours = 0

        if record.work_hours:
            hours = round(
                record.work_hours.total_seconds() /3600,
                2
            )

        total_hours += hours

        if record.status == "Present":
            present += 1

        elif record.status == "Late":
            present += 1
            late += 1

        data.append([
            record.attendance_date.strftime("%d-%m-%Y"),
            record.attendance_date.strftime("%A"),
            record.check_in.strftime("%I:%M %p") if record.check_in else "-",
            record.check_out.strftime("%I:%M %p") if record.check_out else "-",
            f"{hours}h",
            record.status,
        ])

    absent = max(
        calendar.monthrange(year,month)[1] - present,
        0
    )

    data.append([
        "",
        "",
        "",
        "",
        "",
        "",
    ])

    data.append([
        "",
        "",
        "",
        "Present",
        "",
        present
    ])

    data.append([
        "",
        "",
        "",
        "Absent",
        "",
        absent
    ])

    data.append([
        "",
        "",
        "",
        "Late",
        "",
        late
    ])

    data.append([
        "",
        "",
        "",
        "TotalHours",
        "",
        round(total_hours,2)
    ])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#36136E")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.grey),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("BOTTOMPADDING",(0,0),(-1,0),10),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),
    ]))

    elements.append(table)

    doc.build(elements)

    return response