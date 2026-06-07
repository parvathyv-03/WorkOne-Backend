from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated
from .serializers import ChangePasswordSerializer 
from rest_framework.views import APIView

# Create your views here.

@api_view(['POST'])
def login_view(request):

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username,password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)

        return Response({
            'message':'Login successful',
            'access': str(refresh.access_token),
            'refresh':str(refresh),
            'role':user.role,
            'username':user.username,
        })
    
    return Response(
        {'error':'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = ChangePasswordSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        current_password = serializer.validated_data["current_password"]
        new_password = serializer.validated_data["new_password"]

        if not user.check_password(
            current_password
        ):
            return Response(
                {
                    "error":
                    "Current password is incorrect."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(
            new_password
        )

        user.save()

        return Response(
            {
                "message":
                "Password changed successfully."
            }
        )