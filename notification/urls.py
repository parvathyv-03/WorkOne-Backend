from django.urls import path
from .views import NotificationDashboardView

urlpatterns = [
    path("dashboard/",NotificationDashboardView.as_view()),
]