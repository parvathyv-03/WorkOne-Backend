from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LeaveRequest,LeaveBalance
from .serializers import LeaveRequestSerializer

# Create your views here.

class ApplyLeaveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = LeaveRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(
                {"message": "Leave applied succesfully."}
            )

        return Response(
            serializer.errors,
            status=400
        )
    
class LeaveDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        balance,created = LeaveBalance.objects.get_or_create(user=request.user)
        leaves = LeaveRequest.objects.filter(user=request.user).order_by("-applied_on")
        summary = [
            {
                "title" : "Casual Leave Remaining",
                "value": balance.casual_leave,
                "description":"Flexible leave balance"
            },
            {
                "title":"Sick leave Remaining",
                "value": balance.sick_leave,
                "description":"For Medical Leave"
            },
            {
                "title":"Privilege Leave Remaining",
                "value":balance.privilege_leave,
                "description":"Planned leave quota"
            }
        ]

        tracker ={
            "pending": leaves.filter(status="Pending").count(),
            "approved":leaves.filter(status="Approved").count(),
            "rejected":leaves.filter(status="Rejected").count(),
        }

        history = []

        for leave in leaves:
            duration = (leave.end_date - leave.start_date).days + 1
            history.append({
                "type":leave.leave_type,
                "date":leave.applied_on.strftime("%b %d, %Y"),
                "duration":f"{duration} days",
                "status": leave.status,
            })

        return Response({
            "summary":summary,
            "tracker":tracker,
            "history":history
        })
    
class LeaveHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        leaves = LeaveRequest.objects.filter(
            user=request.user
        ).order_by("-applied_on")

        data = []

        for leave in leaves:
            duration = (
                leave.end_date -
                leave.start_date
            ).days + 1

            data.append({
                "type": leave.leave_type,
                "date":leave.applied_on.date(),
                "duration":f"{duration} days",
                "status": leave.status
            })

        return Response(data)
    
class LeaveTrackerView(APIView):
    permission_classes =[IsAuthenticated]

    def get(self,request):
        leaves = LeaveRequest.objects.filter(user=request.user)
        return Response({
            "pending":leaves.filter(status="Pending").count(),
            "approved":leaves.filter(status="Approved").count(),
            "rejected":leaves.filter(status="Rejected").count(),
        })
    
class LeaveSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        balance,created = (
            LeaveBalance.objects.get_or_create(user=request.user)
        )

        return Response({
            "casual_leave": balance.casual_leave,
            "sick_leave":balance.sick_leave,
            "privilege_leave":balance.privilege_leave
        })