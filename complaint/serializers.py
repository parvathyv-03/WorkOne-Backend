from rest_framework import serializers
from .models import Complaint,ComplaintTimeline

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = "__all__"

        read_only_fields = (
            "user",
            "status",
            "created_at"
        )

class ComplaintTimelineSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = ComplaintTimeline
        fields = ["step","created_at"]