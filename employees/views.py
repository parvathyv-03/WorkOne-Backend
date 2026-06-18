from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Employee
from .serializers import EmployeeProfileSerializer
from rest_framework.response import Response

from attendance.models import Attendance
from leave_management.models import LeaveRequest,LeaveBalance
from complaint.models import Complaint
from payslip.models import Payslip
from notification.models import Notification

# Create your views here.

class EmployeeProfileView(RetrieveUpdateAPIView):
    serializer_class =  EmployeeProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Employee.objects.get(user=self.request.user)
    
class EmployeeDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user

        # attendance
        attendance = Attendance.objects.filter(user=user).order_by("-attendance_date").first()
        present_days = Attendance.objects.filter(user=user,status="Present").count()
        
        leave_balance,_=LeaveBalance.objects.get_or_create(user=user)

        pending_complaints = Complaint.objects.filter(user=user,status="Pending").count()
        latest_payslip = Payslip.objects.filter(user=user).order_by("-id").first()
        notifications = Notification.objects.filter(user=user).order_by("-created_at")[:5]
        return Response({
            "attendance":{
                "status":attendance.status if attendance else "Absent",
                "check_in":attendance.check_in if attendance else None,
                "days_present":present_days,
            },

            "leave":{
                "casual":leave_balance.casual_leave,
                "sick":leave_balance.sick_leave,
                "privilege":leave_balance.privilege_leave,
                "total":
                leave_balance.casual_leave +
                leave_balance.sick_leave +
                leave_balance.privilege_leave,
            },

            "complaints":{
                "pending": pending_complaints,
            },
            "payslip":{
                "month":
                latest_payslip.month
                if latest_payslip
                else "N/A"
            },
            "announcements":[
                {
                "id":notification.id,
                "title":notification.title,
                "decription": notification.description,
                "created_at":notification.created_at,
                }
                for notification in notifications
            ],
        })