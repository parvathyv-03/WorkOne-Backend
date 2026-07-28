from django.urls import path
from .views import (
    SummaryAPIView,
    AttendanceAnalyticsAPIView,
    LeaveAnalyticsAPIView,
    ComplaintPayrollAPIView,
    ExportReportAPIView,
)

urlpatterns = [
    path("summary/", SummaryAPIView.as_view(), name="reports-summary"),
    path("attendance/", AttendanceAnalyticsAPIView.as_view(), name="reports-attendance"),
    path("leave/", LeaveAnalyticsAPIView.as_view(), name="reports-leave"),
    path("complaints-payroll/", ComplaintPayrollAPIView.as_view(), name="reports-complaints-payroll"),
    path("export/<str:report_type>/",ExportReportAPIView.as_view(),name="export-report"),
]