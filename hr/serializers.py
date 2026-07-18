from rest_framework import serializers
from accounts.models import User
from employees.models import Employee
from attendance.models import Attendance
from documents.models import EmployeeDocument
from leave_management.models import LeaveRequest
from complaint.models import Complaint,ComplaintTimeline

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
    
class EmployeeListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name =serializers.CharField(source="user.last_name")
    email =serializers.CharField(source="user.email")
    # status = serializers.SerializerMethodField()

    # def get_status(self,obj):
    #     latest = (
    #         Attendance.objects
    #         .filter(user=obj.user)
    #         .order_by("-attendance_date","-check_in")
    #         .first()
    #     )

    #     if latest and latest.check_in and not latest.check_out:
    #         return "Active"
        
    #     return "Inactive"

    class Meta:
        model = Employee
        fields = [
            "employee_id",
            "username",
            "first_name",
            "last_name",
            "email",
            "department",
            "designation",
            "date_of_joining",
            # "status",
        ]
    
class EmployeeUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    username = serializers.CharField(source="user.username",read_only=True)
    role = serializers.CharField(source="user.role",read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "employee_id",
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "marital_status",
            "email",
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
            "username",
            "role",
        ]

    def update(self,instance,validated_data):

        user_data = validated_data.pop("user",{})

        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()

        user = instance.user

        if "first_name" in user_data:
            user.first_name = user_data["first_name"]
        if "last_name" in user_data:
            user.last_name = user_data["last_name"]
        if "email" in user_data:
            user.email = user_data["email"]

        user.save()

        return instance

class HRDocumentSerializer(serializers.ModelSerializer):

    employee_id = serializers.CharField(source="user.employee.employee_id",read_only=True)
    employee_name = serializers.SerializerMethodField()

    document_url = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeDocument
        fields = [
            "id",
            "employee_id",
            "employee_name",
            "category",
            "description",
            "status",
            "uploaded_at",
            "document_url",
        ]   

    def get_employee_name(self,obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    def get_document_url(self,obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.document.url)
        return obj.document.url


# FOR HR LEAVE REQUEST APPROVAL,REJECTION

class HRLeaveSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    employee_id = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    total_days = serializers.SerializerMethodField()

    class Meta:
         model = LeaveRequest
         fields = [
             "id",
             "employee_name",
             "employee_id",
             "department",
             "leave_type",
             "start_date",
             "end_date",
             "reason",
             "status",
             "applied_on",
             "total_days",
         ]


    def get_employee_name(self,obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    def get_employee_id(self,obj):
        return obj.user.employee.employee_id
    
    def get_department(self,obj):
        return obj.user.employee.department
    
    def get_total_days(self,obj):
        return obj.total_days()
    
    # HR COMPLAINT DASHBOARD 
    
class HRComplaintSerializer(serializers.ModelSerializer):

    employee_name = serializers.SerializerMethodField()
    employee_id = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Complaint
        fields = [
            "id",
            "employee_name",
            "employee_id",
            "department",
            "category",
            "subject",
            "description",
            "status",
            "created_at",
        ]

    def get_employee_name(self,obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    def get_employee_id(self,obj):
        return obj.user.employee.employee_id
    
    def get_department(self,obj):
        return obj.user.employee.department
    
class ComplaintTimelineSerializer(serializers.ModelSerializer):
    complaint_id = serializers.IntegerField(source="complaint.id")

    class Meta:
        model = ComplaintTimeline
        fields=[
            "id",
            "complaint_id",
            "step",
            "created_at",
        ]

class ComplaintTimelineSerializer(serializers.ModelSerializer):

    complaint_id = serializers.IntegerField(source="complaint.id")

    class Meta:
        model = ComplaintTimeline
        fields = [
            "id",
            "complaint_id",
            "step",
            "created_at",
        ]