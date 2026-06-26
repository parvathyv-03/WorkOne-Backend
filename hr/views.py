from rest_framework.views import APIView
from rest_framework.response import Response
from employees.models import Employee
from accounts.models import User
from attendance.models import Attendance
from .serializers import CreateEmployeeSerializer
from rest_framework.permissions import IsAuthenticated


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
        # data = serializer.validated_data

        # user = User.objects.create_user(
        #     username=data["username"],
        #     password=data["password"],
        #     first_name=data["first_name"],
        #     last_name=data["last_name"],
        #     email=data["email"],
        #     role="employee"
        # )

        # Employee.objects.create(
        #     user=user,
        #     employee_id=data["employee_id"],
        #     department=data["department"],
        #     designation=data["designation"],
        #     employee_type=data["employee_type"],
        #     date_of_joining=data["date_of_joining"],
        #     mobile_number=data["mobile_number"],
        #     gender=data["gender"],
        #     marital_status=data["marital_status"],
        #     current_address="",
        #     permanent_address="",
        #     reporting_manager="",
        #     emergency_contact_name="",
        #     emergency_relationship="",
        #     emergency_contact_number=""
        # )

        # return Response(
        #     {"message":"Employee created succesfully."}
        # )