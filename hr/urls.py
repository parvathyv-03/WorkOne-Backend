from django.urls import path
from .views import CreateEmployeeView,EmployeeListView,export_employees_pdf,EmployeeDetailView

urlpatterns = [
   path("create-employee/",CreateEmployeeView.as_view()),
   path("employees/",EmployeeListView.as_view(),name="employee-list"),
   path("employees/export-pdf/",export_employees_pdf,name="export-employees-pdf"),
   path("employees/<str:employee_id>/",EmployeeDetailView.as_view(),name="employee-detail"),
]  