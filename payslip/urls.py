from django.urls import path
from .views import PayslipDashboardView

urlpatterns = [
    path( "dashboard/",PayslipDashboardView.as_view()),
]