from django.urls import path
from .views import(CheckInView,CheckOutView,AttendanceStatusView,AttendanceHistoryView)

urlpatterns=[
    path ("attendance/check-in/",CheckInView.as_view()),
    path ("attendance/check-out/",CheckOutView.as_view()),
    path("attendance/status/",AttendanceStatusView.as_view()),
    path("attendance/history/",AttendanceHistoryView.as_view()),
]