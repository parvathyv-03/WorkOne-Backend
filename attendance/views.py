from datetime import time
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
    
class MonthlyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        month = int(request.GET.get("month"))
        year = int(request.GET.get("year"))

        attendance_records = Attendance.objects.filter(
            user=request.user,
            attendance_date__month=month,
            attendance_date__year=year
        ).order_by("attendance_date")

        rows= []

        present_days = 0
        absent_days = 0
        late_days =0
        total_hours = 0

        for record in attendance_records:
            work_hours = 0
            if record.work_hours is not None:
                work_hours = round(
                    record.work_hours.total_seconds()/3600,
                    2
                )
            
            total_hours += work_hours

            if record.status == "Present":
                present_days += 1
            
            elif record.status == "Absent":
                absent_days += 1
            
            elif record.status == "Late":
                late_days += 1

            rows.append({
                "date": record.attendance_date,
                "day": record.attendance_date.strftime("%a"),
                "checkIn": record.check_in.strftime("%I :%M %p") if record.check_in else "-",
                "checkOut": record.check_out.strftime("%I :%M %p") if record.check_out else "-",
                "workHours":f"{work_hours}h",
                "status":record.status
            })

        summary = {
            "present_days":present_days,
            "absent_days": absent_days,
            "late_days":late_days,
            "total_hours":total_hours
        }

        attendance_percentage = 0

        total_days = present_days + late_days + absent_days 

        if total_days > 0:
            attendance_percentage = round(
                ((present_days + late_days)/total_days) * 100,
                2
            )

        checkin_records = [
            record.check_in.time()
            for record in attendance_records
            if record.check_in
        ]
        avg_check_in = "-"

        if checkin_records:
            total_minutes = sum(
                t.hour * 60 + t.minute
                for t in checkin_records
            )

            avg_minutes = total_minutes // len(checkin_records)

            avg_hour = avg_minutes // 60
            avg_minute = avg_minutes %60

            avg_check_in = time(avg_hour,avg_minute).strftime("%I:%M %p")

        checkout_records = [
            record.check_out.time()
            for record in attendance_records
            if record.check_out
        ]

        avg_check_out = "-"

        if checkout_records:
            total_minutes = sum(
                t.hour * 60 + t.minute
                for t in checkout_records
            )

            avg_minutes = total_minutes // len(checkout_records)

            avg_hour = avg_minutes //60
            avg_minute = avg_minutes % 60

            avg_check_out = f"{avg_hour:02}:{avg_minute:02}"

        overtime_hours = 0

        for record in attendance_records:
            if record.work_hours:
                worked = record.work_hours.total_seconds()/3600

                if worked > 8:
                    overtime_hours += worked - 8

        best_streak = 0
        current_streak = 0

        for record in attendance_records:
            if record.status in ["Present","Late"]:
                current_streak += 1
                best_streak = max(best_streak,current_streak)
            else:
                current_streak = 0

        stats = [
            {
                "label":"Attendance Percentage",
                "value":f"{attendance_percentage}%"
            },
            {
                "label":"Avg Check-In Time",
                "value":avg_check_in
            },
            {
                "label":"Avg Check-Out Time",
                "value":avg_check_out
            },
            {
                "label":"Total Working Hours",
                "value":f"{round(total_hours,2)}h"
            },
            {
                "label":"Overtime Hours",
                "value":f"{round(overtime_hours,2)}h"
            },
            {
                "label":"Late Arrivals",
                "value":late_days
            },
        ]

        insights = [
            {
                "label":"Best Attendance Streak",
                "value":f"{best_streak} days"
            },
            {
                "label":"Total Present Days",
                "value":f"{present_days} days"
            },
            {
                "label":"Total Absent Days",
                "value":f"{absent_days} days"
            },
            {
                "label":"Total Late Arrivals",
                "value":f"{late_days} times"
            }
        ]

        return Response({
            "summary":summary,
            "stats":stats,
            "insights":insights,
            "rows":rows
        })