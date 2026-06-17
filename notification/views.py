from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
# Create your views here.

class NotificationDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):

        notifications = Notification.objects.filter(user=request.user).order_by("-created_at")

        summary = [
            {
                "title":"Leave Updates",
                "count":notifications.filter(category="Leave").count(),
            },
            {
                "title":"Complaint Updates",
                "count":notifications.filter(category="Complaint").count(),
            },
            {
                "title":"HR Announcements",
                "count":notifications.filter(category="HR Announcement").count(),
            },
            {
                "title":"System Notifications",
                "count":notifications.filter(category="System").count(),
            },
        ]

        recent_notifications = []

        for n in notifications:
            recent_notifications.append({
                "title":n.title,
                "description":n.description,
                "category":n.category,
                "time":n.created_at.strftime("%b %d,%Y"),
            })

        return Response({
            "summary":summary,
            "notifications":recent_notifications,
        })
    