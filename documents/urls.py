from django.urls import path

from .views import(EmployeeDocumentListView,ReplaceDocumentView,UploadDocumentView)

urlpatterns = [
    path("employee/documents/",EmployeeDocumentListView.as_view()),
    path("employee/documents/<int:pk>/replace/",ReplaceDocumentView.as_view()),
    path("employee/documents/upload/",UploadDocumentView.as_view())
]

