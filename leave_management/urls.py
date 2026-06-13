from django.urls import path

from .views import(ApplyLeaveView,LeaveHistoryView,LeaveTrackerView,LeaveSummaryView,LeaveDashboardView)

urlpatterns = [
    path("apply/",ApplyLeaveView.as_view()),
    path("history/",LeaveHistoryView.as_view()),
    path("tracker/",LeaveTrackerView.as_view()),
    path("summary/",LeaveSummaryView.as_view()),
    path("dashboard/",LeaveDashboardView.as_view()),
]