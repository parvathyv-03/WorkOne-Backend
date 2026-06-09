from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import EmployeeDocument
from .serializers import(EmployeeDocumentSerializer)

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class EmployeeDocumentListView(ListAPIView):
    serializer_class = (EmployeeDocumentSerializer)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EmployeeDocument.objects.filter(user=self.request.user)

class ReplaceDocumentView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self,request,pk):

        document = EmployeeDocument.objects.get(id=pk,user=request.user)
        uploaded_file = request.FILES.get("document")

        if uploaded_file:
            document.document = uploaded_file
            document.status = ("Pending Verification")

            document.save()

        return Response(
            {
                "message":
                "Document replaced succesfully."
            }
        )
    
class UploadDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        document = EmployeeDocument.objects.create(
            user=request.user,
            category=request.data.get("category"),
            description=request.data.get("description"),
            document=request.FILES.get("document"),
        )

        return Response({
            "message":"document uploaded successfully.",
            "id": document.id
        })