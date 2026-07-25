from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import JobOpening
from .serializers import JobOpeningSerializer

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

        return Response(
            {
                "count":jobs.count(),
                "results":serializer.data
            },
            status=status.HTTP_200_OK
        )