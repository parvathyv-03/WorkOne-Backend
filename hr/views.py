from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from employees.models import Employee
from accounts.models import User
from attendance.models import Attendance
from .serializers import CreateEmployeeSerializer,EmployeeListSerializer,EmployeeUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view

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

        if latest_attendance and latest_attendance.check_in and not latest_attendance.check_out:
            status = "Active"
        else:
            status = "Inactive"

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