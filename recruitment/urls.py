from django.urls import path
from .views import CreateJobAPIView,JobListAPIView

urlpatterns = [
    path("jobs/create/",CreateJobAPIView.as_view(),name="create-job"),
    path("jobs/",JobListAPIView.as_view(),name="job-list"),
]