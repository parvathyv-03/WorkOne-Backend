from django.urls import path
from .views import EmployeeProfileView,EmployeeDashboardView

urlpatterns = [
    path("employee/profile/",EmployeeProfileView.as_view(),name="employee-profile"),
    path("employee/dashboard/",EmployeeDashboardView.as_view()),
]