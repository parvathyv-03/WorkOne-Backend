from django.urls import path
from .views import(CheckInView,CheckOutView,AttendanceStatusView,AttendanceHistoryView,MonthlyReportView,AttendanceCalendarView,RecentAttendanceView,AttendanceSummaryView)

urlpatterns=[
    path ("attendance/check-in/",CheckInView.as_view()),
    path ("attendance/check-out/",CheckOutView.as_view()),
    path("attendance/status/",AttendanceStatusView.as_view()),
    path("attendance/history/",AttendanceHistoryView.as_view()),
    path("attendance/monthly-report/",MonthlyReportView.as_view()),
    path("attendance/calendar/",AttendanceCalendarView.as_view()),
    path("attendance/recent/",RecentAttendanceView.as_view()),
    path("attendance/summary/",AttendanceSummaryView.as_view()),
]