from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import TotalScore

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required = True
    )
    class Meta:
        model = User
        fields = ('username', 'password')
    
    def create(self, validated_data):
        user=User.objects.create_user(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = User
        fields = ('username', 'password')
    def validate(self, data):
        user=authenticate(**data)
        if user:
            User.objects.get(username=user)
            return user
        raise serializers.ValidationError(
            {"error":"This user is not exists"}
        )
        
class TotalScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalScore
        fields = ("user", "total_score")
        