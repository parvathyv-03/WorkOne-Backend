from django.urls import path
from .views import CreateJobAPIView,JobListAPIView,JobDetailAPIView,CandidateListCreateAPIView,CandidateStatusUpdateAPIView,DeleteCandidateAPIView,DeleteJobAPIView

urlpatterns = [
    path("jobs/create/",CreateJobAPIView.as_view(),name="create-job"),
    path("jobs/",JobListAPIView.as_view(),name="job-list"),
    path("jobs/<int:job_id>/",JobDetailAPIView.as_view(),name="job-detail"),
    path("jobs/<int:job_id>/candidates/",CandidateListCreateAPIView.as_view(),name="candidate-list-create"),
    path("candidates/<int:candidate_id>/status/",CandidateStatusUpdateAPIView.as_view(),name="candidate-status-update"),
    path("candidates/<int:candidate_id>/delete/",DeleteCandidateAPIView.as_view(),name="candidate-delete"),
    path("jobs/<int:job_id>/delete/",DeleteJobAPIView.as_view())
]