from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import TotalScore


class RegisterSerializer(serializers.ModelSerializer):
    """
    author : 임혁
    explanation : 회원가입 관련 시리얼라이저
    """
    password = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        """
        author : 임혁
        explanation : 회원가입 시 사용자 정보를 등록하는 함수
        """
        user=User.objects.create_user(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    """
    author : 임혁
    explanation : 로그인할 경우 필요한 필드 정보를 위한 시리얼라이저
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, data):
        """
        author : 임혁
        explanation : 로그인 인증, 등록된 사용자가 맞는지 검증하는 함수
        """
        user=authenticate(**data)
        if user:
            User.objects.get(username=user)
            return user
        raise serializers.ValidationError(
            {"error":"This user is not exists"}
        )


class TotalScoreSerializer(serializers.ModelSerializer):
    """
    유저 총합 점수 시리얼라이저
    """

    class Meta:
        model = TotalScore
        fields = [
            'total_score'
        ]