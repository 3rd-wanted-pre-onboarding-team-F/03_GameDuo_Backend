from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import LoginSerializer, RegisterSerializer
from drf_yasg.utils import swagger_auto_schema
from .user_api_params import user_post_params




class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    @swagger_auto_schema(request_body=user_post_params)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class UserView(generics.RetrieveAPIView):
    serializer_class = LoginSerializer
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        if user:
            return Response(LoginSerializer(user).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)