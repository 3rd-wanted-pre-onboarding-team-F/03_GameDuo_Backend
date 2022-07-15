from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, mixins, viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Sum

from .user_api_params import user_post_params
from .serializers import LoginSerializer, RegisterSerializer, TotalScoreSerializer
from user.models import User, TotalScore
from bossRaid.models import BossRaidHistory
from bossRaid.serializers import BossRaidHistorySerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
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


class TotalScoreAPI(mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """
    author : 이승민
    request : Dict
    response : Dict, status code
    explanation :
        유저 조회 뷰
        - 해당 유저의 id
        - 해당 유저의 총합 점수
        aggregate 함수를 사용해서 Boss raid history에 해다 유저의 점수를 전부 더한다.
    """

    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return TotalScoreSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs['user_id']
        user_id = get_object_or_404(User, pk=pk)
        history = BossRaidHistory.objects.filter(user_id=user_id).all()
        boss_history = BossRaidHistorySerializer(history, many=True)

        """ 사용자 상세 조회 시 총합 점수 및 히스토리 반환 """
        user = TotalScore.objects.get(user_id=pk)
        sum = BossRaidHistory.objects.aggregate(Sum('score'))['score__sum']
        user.total_score = sum
        user.save()

        res = {
            'totalScore': sum,
            'bossRaidHistory': boss_history.data
        }

        return Response(res, status=status.HTTP_200_OK)

