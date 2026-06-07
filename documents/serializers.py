from rest_framework import serializers
from .models import EmployeeDocument

class EmployeeDocumentSerializer(serializers.ModelSerializer):
    document_url = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeDocument
        fields = ["id","category","description","status","uploaded_at","updated_at","document","document_url",]

    def get_document_url(self,obj):
        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(obj.document.url)
        return obj.document.url