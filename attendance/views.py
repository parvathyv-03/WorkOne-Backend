from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import AttendanceSerializer

from .models import Attendance
# Create your views here.

class CheckInView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        today = timezone.now().date()
        existing = Attendance.objects.filter(user=request.user,attendance_date=today).first()

        if existing:
            return Response(
                {
                    "message":
                    "Already checked in"
                },
                status=400
            )
        
        Attendance.objects.create(user=request.user,check_in=timezone.now())

        return Response(
            {
                "message":
                "Checked In"
            }
        )

class CheckOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        today = timezone.now().date()
        attendance = Attendance.objects.filter(user=request.user,attendance_date=today).first()

        if not attendance:
            return Response(
                {
                    "message":
                    "Check in first"
                },
                status=400
            )
        
        if attendance.check_out:
            return Response(
                {
                    "message":
                    "Already checked out"
                },
                status=400
            )
        
        attendance.check_out = timezone.now()

        attendance.work_hours = (attendance.check_out- attendance.check_in)

        attendance.save()

        return Response(
            {
                "message":
                "Checked Out"
            }
        )
    

class AttendanceStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        today = timezone.now().date()
        attendance = Attendance.objects.filter(user=request.user,attendance_date=today).first()

        if not attendance:
            return Response(
                {
                    "checked_in":False
                }
            )
        
        return Response(
            {
                "checked_in":True,
                "check_in":
                attendance.check_in,
                "checked_out":
                attendance.check_out is not None
            }
        )
    
class AttendanceHistoryView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        attendance = Attendance.objects.filter(user=request.user).order_by("-attendance_date")
        serializer = AttendanceSerializer ( attendance,many=True)

        return Response(serializer.data)