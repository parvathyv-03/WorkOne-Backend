from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Employee
from .serializers import EmployeeProfileSerializer

# Create your views here.

class EmployeeProfileView(RetrieveAPIView):
    serializer_class =  EmployeeProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Employee.objects.get(user=self.request.user)
