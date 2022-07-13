from rest_framework import serializers
from .models import User, TotalScore


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class TotalScoreSerializer(serializers.ModelSerializer):
    """
    유저 총합 점수 시리얼라이저
    """

    class Meta:
        model = TotalScore
        fields = [
            'total_score'
        ]
        
