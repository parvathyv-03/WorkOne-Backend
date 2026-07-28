from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count,Sum

from employees.models import Employee
from attendance.models import Attendance
from leave_management.models import LeaveRequest
from complaint.models import Complaint
from payslip.models import Payslip
from django.http import HttpResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (SimpleDocTemplate,Table,TableStyle,Paragraph,)

from reportlab.lib.styles import getSampleStyleSheet

# Create your views here.

class SummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        total_employees = Employee.objects.count()

        present =Attendance.objects.filter(status="Present").count()
        total_attendance = Attendance.objects.count()

        attendance_rate = (
            round((present/total_attendance) * 100,1)
            if total_attendance > 0 else 0
        ) 

        leave_requests = LeaveRequest.objects.filter(status="Pending").count()

        open_complaints = Complaint.objects.filter(status="Resolved").count()

        payroll_processed = Payslip.objects.exclude(status="Paid").count()

        active_departments = (Employee.objects.values("department").distinct().count())

        return Response({
            "total_employees":total_employees,
            "attendance_rate":attendance_rate,
            "leave_requests":leave_requests,
            "open_complaints":open_complaints,
            "payroll_processed":payroll_processed,
            "active_departments":active_departments,
        })

class AttendanceAnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):

        total = Attendance.objects.count()

        present = Attendance.objects.filter(status="Present").count()
        absent = Attendance.objects.filter(status="Absent").count()
        late = Attendance.objects.filter(status="Late").count()

        def percentage(value):
            return round((value/total) * 100,1) if total else 0

        data = [
            {
                "label": "Present",
                "value": percentage(present),
                "count": present,
                "color": "bg-green-500"
            },
            {
                "label": "Absent",
                "value": percentage(absent),
                "count": absent,
                "color": "bg-red-500"
            },
            {
                "label": "Late Entries",
                "value": percentage(late),
                "count": late,
                "color": "bg-orange-500"
            }
        ]

        return Response(data)

class LeaveAnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        total = LeaveRequest.objects.count()

        casual = LeaveRequest.objects.filter(leave_type="Casual Leave").count()
        sick = LeaveRequest.objects.filter(leave_type="Sick Leave").count()
        privilege = LeaveRequest.objects.filter(leave_type="Privilege Leave").count()
        pending = LeaveRequest.objects.filter(status="Pending").count()

        def percentage(value):
            return round((value/total) * 100,1) if total else 0

        data = [
            {
                "label": "Casual Leave Usage",
                "value": percentage(casual),
                "count": casual,
                "color": "bg-violet-600"
            },
            {
                "label": "Sick Leave Usage",
                "value": percentage(sick),
                "count": sick,
                "color": "bg-sky-500"
            },
            {
                "label": "Privilege Leave Usage",
                "value": percentage(privilege),
                "count": privilege,
                "color": "bg-pink-500"
            },
            {
                "label": "Pending Leave Requests",
                "value": percentage(pending),
                "count": pending,
                "color": "bg-yellow-500"
            }
        ]

        return Response(data)

class ComplaintPayrollAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):

        total_complaints = Complaint.objects.count()

        resolved = Complaint.objects.filter(status="Resolved").count()
        pending = Complaint.objects.filter(status="Pending").count()
        escalated = Complaint.objects.filter(status="Escalated").count()

        def complaint_percentage(value):
            return round((value/total_complaints) * 100,1) if total_complaints else 0

        complaints = [
            {
                "label": "Total Complaints",
                "value": total_complaints,
                "percent": "100%"
            },
            {
                "label": "Resolved",
                "value": resolved,
                "percent": f"{complaint_percentage(resolved)}%"
            },
            {
                "label": "Pending",
                "value": pending,
                "percent": f"{complaint_percentage(pending)}%"
            },
            {
                "label": "Escalated",
                "value": escalated,
                "percent": f"{complaint_percentage(escalated)}%"
            }
        ] 

        payroll = Payslip.objects.aggregate(
            salary=Sum("net_salary"),
            bonus=Sum("bonus"),
            deductions=Sum("total_deductions")
        )

        payroll_data = [
            {
                "label": "Total Salary Processed",
                "value": payroll["salary"] or 0
            },
            {
                "label": "Total Bonuses",
                "value": payroll["bonus"] or 0
            },
            {
                "label": "Total Deductions",
                "value": payroll["deductions"] or 0
            },
            {
                "label": "Payslips Generated",
                "value": Payslip.objects.count()
            }
        ]

        return Response({
            "complaints":complaints,
            "payroll":payroll_data
        })

class ExportReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,report_type):
        response = HttpResponse(content_type="application/pdf")

        response["Content-Disposition"] = (f'inline; filename="{report_type}_report.pdf"')

        doc = SimpleDocTemplate(response,pagesize=landscape(A4))

        styles = getSampleStyleSheet()

        elements = []

        elements.append(Paragraph(f"<b>{report_type.replace('_',' ').title()} Report</b>",styles["Heading1"]))

        if report_type == "employees":
            data = [
                [
                    "Employee ID",
                    "Name",
                    "Department",
                    "Designation",
                    "Employee Type",
                ]
            ]

            employees = Employee.objects.select_related("user")

            for emp in employees:
                data.append([
                    emp.employee_id,
                    emp.user.get_full_name() or emp.user.username,
                    emp.department,
                    emp.designation,
                    emp.employee_type,
                ])

        elif report_type == "attendance":
            data = [
                [
                    "Employee",
                    "Date",
                    "Check In",
                    "Check Out",
                    "Status",
                ]
            ]

            records = Attendance.objects.select_related("user")

            for item in records:
                data.append([
                    item.user.get_full_name() or item.user.username,
                    str(item.attendance_date),
                    str(item.check_in.time()) if item.check_in else "-",
                    str(item.check_out.time()) if item.check_out else "-",
                    item.status,
                ])

        elif report_type == "leaves":

            data = [
                [
                    "Employee",
                    "Leave Type",
                    "Start Date",
                    "End Date",
                    "Status",
                ]
            ]

            leaves = LeaveRequest.objects.select_related("user")

            for leave in leaves:

                data.append([
                    leave.user.get_full_name() or leave.user.username,
                    leave.leave_type,
                    str(leave.start_date),
                    str(leave.end_date),
                    leave.status,
                ])

        elif report_type == "complaints":

            data = [
                [
                    "Employee",
                    "Category",
                    "Subject",
                    "Status",
                ]
            ]

            complaints = Complaint.objects.select_related("user")

            for complaint in complaints:

                data.append([
                    complaint.user.get_full_name() or complaint.user.username,
                    complaint.category,
                    complaint.subject,
                    complaint.status,
                ])

        elif report_type == "payroll":

            data = [
                [
                    "Employee",
                    "Month",
                    "Net Salary",
                    "Bonus",
                    "Status",
                ]
            ]

            payslips = Payslip.objects.select_related("user")

            for pay in payslips:
                data.append([
                    pay.user.get_full_name() or pay.user.username,
                    pay.month,
                    f"₹ {pay.net_salary}",
                    f"₹ {pay.bonus}",
                    pay.status,
                ])

        else:

            return Response(
                {"error":"Invalid report type."},
                status=400
            )

        table = Table(data)

        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#36136E")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ])
        )

        elements.append(table)

        doc.build(elements)

        return response