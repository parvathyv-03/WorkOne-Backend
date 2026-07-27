from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import JobOpening,CandidateApplication
from .serializers import JobOpeningSerializer,CandidateSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Count

# Create your views here.

class CreateJobAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):

        serializer = JobOpeningSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message":"Job created successfully.",
                    "data":serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status= status.HTTP_400_BAD_REQUEST
        )
    
class JobListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        jobs = JobOpening.objects.all().order_by("created_at")

        serializer = JobOpeningSerializer(jobs,many=True)

        summary = {
            "open_positions":jobs.filter(status="Open").count(),
            "total_applications":CandidateApplication.objects.count(),
            "interviews_scheduled": CandidateApplication.objects.filter(status="Interview").count(),
            "hired_candidates":CandidateApplication.objects.filter(status="Hired").count(),
        }

        return Response(
            {
                "count":jobs.count(),
                "summary":summary,
                "results":serializer.data
            },
            status=status.HTTP_200_OK,
        )

class JobDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,job_id):
        job = get_object_or_404(JobOpening,id=job_id)

        serializer = JobOpeningSerializer(job)

        return Response(serializer.data,status=status.HTTP_200_OK)

class CandidateListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,job_id):
        job = get_object_or_404(JobOpening,id=job_id)

        candidates = CandidateApplication.objects.filter(job=job).order_by("-created_at")

        serializer = CandidateSerializer(candidates,many=True)

        return Response(
            {
                "count": candidates.count(),
                "results":serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self,request,job_id):
        job = get_object_or_404(JobOpening,id=job_id)

        serializer = CandidateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(job=job)

            return Response(
                {
                    "message":"Candidate added successfully.",
                    "data":serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class CandidateStatusUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self,request,candidate_id):
        candidate = get_object_or_404(
            CandidateApplication,
            id=candidate_id
        )

        status_value = request.data.get("status")

        if status_value:
            candidate.status = status_value
            candidate.save()

        serializer = CandidateSerializer(candidate)

        return Response(
            {
                "message": "Candidate status updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class DeleteCandidateAPIView(APIView):
    permission_classes= [IsAuthenticated]

    def delete(self,request,candidate_id):
        candidate = get_object_or_404(
            CandidateApplication,
            id=candidate_id
        )

        candidate.delete()

        return Response(
            {
                "message": "Candidate updated successfully."
            },
            status=status.HTTP_200_OK,
        )

class DeleteJobAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request,job_id):
        job= get_object_or_404(JobOpening,id=job_id)

        job.delete()

        return Response(
            {"message":"Job deleted successfully."},
            status=status.HTTP_200_OK,
        )