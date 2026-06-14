from django.urls import path
from .views import(ComplaintCreateView,ComplaintDashboardView,ComplaintTimelineView)

urlpatterns = [
    path("create/",ComplaintCreateView.as_view()),
    path("dashboard/",ComplaintDashboardView.as_view()),
    path("timeline/<int:complaint_id>/",ComplaintTimelineView.as_view()),
]