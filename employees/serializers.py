from rest_framework import serializers
from .models import Employee

class EmployeeProfileSerializer(
    serializers.ModelSerializer
):
    full_name = serializers.SerializerMethodField()

    email = serializers.EmailField(
        source='user.email'
    )

    class Meta:
        model = Employee

        fields = [
            "employee_id",
            "full_name",
            "email",
            "date_of_birth",
            "gender",
            "marital_status",
            "mobile_number",
            "alternate_number",
            "current_address",
            "permanent_address",
            "department",
            "designation",
            "employee_type",
            "date_of_joining",
            "reporting_manager",
            "emergency_contact_name",
            "emergency_relationship",
            "emergency_contact_number",
            "emergency_alternate_number",
        ]

    def get_full_name(self,obj):
            return f"{obj.user.first_name} {obj.user.last_name}"