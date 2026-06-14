from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Complaint
from .models import ComplaintTimeline
from .serializers import ComplaintSerializer

# Create your views here.

class ComplaintCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = ComplaintSerializer(data=request.data)

        if serializer.is_valid():
            complaint = serializer.save(user=request.user)
            ComplaintTimeline.objects.create(complaint=complaint,step="Complaint Submitted")

            return Response({
                "message":"Complaint submitted succesfully"
            })
        return Response(serializer.errors,status=400)
    

class ComplaintDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        
        complaints = Complaint.objects.filter(user=request.user).order_by("-created_at")

        summary = [
            {
                "title":"Total Complaints",
                "value":complaints.count()
            },
            {
                "title":"Pending",
                "value":complaints.filter(status="Pending").count()
            },
            {
                "title":"In Review",
                "value":complaints.filter(status="In Review").count()
            },
            {
                "title":"Resolved",
                "value":complaints.filter(status="Resolved").count()
            }
        ]

        complaint_data = []

        for complaint in complaints:

            complaint_data.append({
                "id":f"CMP-{complaint.id:04d}",
                "category": complaint.category,
                "subject": complaint.subject,
                "description": complaint.description,
                "date": complaint.created_at.strftime("%b %d,%Y"),
                "status": complaint.status
            })

        return Response({
            "summary": summary,
            "complaints": complaint_data
        })
    
class ComplaintTimelineView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,complaint_id):
        complaint = Complaint.objects.get(id=complaint_id,user=request.user)
        timeline = []

        for item in complaint.timeline.all():
            timeline.append({
                "step":item.step,
                "date": item.created_at
            })

        return Response({
            "id": complaint.id,
            "status": complaint.status,
            "timeline": timeline
        })