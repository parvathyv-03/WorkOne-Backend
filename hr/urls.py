from django.urls import path
from .views import CreateEmployeeView,EmployeeListView,export_employees_pdf,EmployeeDetailView,HRDocumentListView,VerifyDocumentView,HRLeaveListAPIView,HRLeaveDetailAPIView,ApproveLeaveAPIView,RejectLeaveAPIView,HRComplaintListAPIView,UpdateComplaintStatusAPIView,HRComplaintDetailAPIView,ComplaintTimelineAPIView,AttendanceAnalyticsView,HRAttendanceListView,HRAttendanceSummaryView,HRWeeklyAttendanceGraphView,hr_monthly_attendance_pdf,HRNotificationListAPIView,PublishNotificationApiView,DeleteNotificationAPIView,HRPayslipAPIView

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
   path("complaints/list/",HRComplaintListAPIView.as_view()),
   path("complaints/<int:pk>/",HRComplaintDetailAPIView.as_view()),
   path("complaints/update/<int:pk>/",UpdateComplaintStatusAPIView.as_view()),
   path("complaints/activity/",ComplaintTimelineAPIView.as_view()),
   path("attendance/analytics/",AttendanceAnalyticsView.as_view()),
   path("attendance/summary/",HRAttendanceSummaryView.as_view()),
   path("attendance/list/",HRAttendanceListView.as_view()),
   path("attendance/weekly-graph/",HRWeeklyAttendanceGraphView.as_view()),
   path("attendance/monthly-report/pdf/",hr_monthly_attendance_pdf),
   path("notifications/list/",HRNotificationListAPIView.as_view()),
   path("notifications/publish/",PublishNotificationApiView.as_view()),
   path("notifications/delete/<uuid:group_id>/",DeleteNotificationAPIView.as_view()),
   path("payslips/list/",HRPayslipAPIView.as_view()),
]