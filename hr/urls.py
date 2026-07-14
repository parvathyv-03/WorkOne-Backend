from django.urls import path
from .views import CreateEmployeeView,EmployeeListView,export_employees_pdf,EmployeeDetailView,HRDocumentListView,VerifyDocumentView,HRLeaveListAPIView,HRLeaveDetailAPIView,ApproveLeaveAPIView,RejectLeaveAPIView,HRComplaintListAPIView,UpdateComplaintStatusAPIView,HRComplaintDetailAPIView

urlpatterns = [
   path("create-employee/",CreateEmployeeView.as_view()),
   path("employees/",EmployeeListView.as_view(),name="employee-list"),
   path("employees/export-pdf/",export_employees_pdf,name="export-employees-pdf"),
   path("employees/<str:employee_id>/",EmployeeDetailView.as_view(),name="employee-detail"),
   path("documents/",HRDocumentListView.as_view()),
   path("documents/<int:pk>/verify/",VerifyDocumentView.as_view()),
   path("leaves/",HRLeaveListAPIView.as_view(),name="hr-leaves"),
   path("leaves/<int:pk>/",HRLeaveDetailAPIView.as_view()),
   path("leaves/<int:pk>/approve",ApproveLeaveAPIView.as_view()),
   path("leaves/<int:pk>/reject",RejectLeaveAPIView.as_view()),
   path("hr/list/",HRComplaintListAPIView.as_view()),
   path("hr/<int:pk>/",HRComplaintDetailAPIView.as_view()),
   path("hr/update/<int:pk>/",UpdateComplaintStatusAPIView.as_view()),
]  