from rest_framework import serializers
from .models import User, TotalScore

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        

class TotalScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalScore
        fields = ['id', 'user', 'total_score']
        
