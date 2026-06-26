from rest_framework import serializers
from accounts.models import User
from employees.models import Employee

class CreateEmployeeSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()

    employee_id = serializers.CharField()

    date_of_birth = serializers.DateField(required=False)

    gender = serializers.CharField()
    marital_status = serializers.CharField()

    mobile_number = serializers.CharField()
    alternate_number = serializers.CharField(
        required=False,
        allow_blank=True
    )

    current_address = serializers.CharField()
    permanent_address = serializers.CharField()

    department = serializers.CharField()
    designation = serializers.CharField()
    employee_type = serializers.CharField()
    date_of_joining = serializers.DateField()

    reporting_manager = serializers.CharField()

    emergency_contact_name = serializers.CharField()
    emergency_relationship = serializers.CharField()
    emergency_contact_number = serializers.CharField()

    emergency_alternate_number = serializers.CharField(
        required=False,
        allow_blank=True
    )

    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists."
            )
        return value
    
    def validate_employee_id(self,value):

        if Employee.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError(
                "Employee ID already exists."
            )
        return value
    
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def create(self,validated_data):
        password = validated_data.pop("password")

        username = validated_data.pop("username")
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        email = validated_data.pop("email")

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role="employee"
        )

        employee = Employee.objects.create(user=user,**validated_data)
        
        return employee