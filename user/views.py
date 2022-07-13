from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .user_api_params import user_post_params
from .serializers import LoginSerializer, RegisterSerializer, TotalScoreSerializer
from .models import TotalScore



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
    
class TotalScoreView(generics.RetrieveUpdateAPIView):
    queryset = TotalScore.objects.all()
    serializer_class = TotalScoreSerializer