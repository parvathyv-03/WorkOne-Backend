from rest_framework import serializers
from .models import JobOpening,CandidateApplication

class JobOpeningSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobOpening
        fields = "__all__"

class CandidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateApplication
        fields = "__all__"
        read_only_fields = ["job"]