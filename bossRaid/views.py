# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.cache import cache
from django.db import transaction
from bossRaid.serializers import (
    BossRaidStartSerializer,
    BossRaidEndSerializer,
    BossRaidStatusSerializer,
    BossRaidSerializer,
)
from bossRaid.models import (
    BossRaidHistory,
    BossRaidStatus,
    BossRaid,
)
from user.serializers import TotalScoreSerializer
from user.models import (
    TotalScore,
    User,
)
from .services import RankingDataService

import requests
import json


class BossRaidAPI(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    author : 이승민
    reqeust : Dict
    response : Dict, status code
    explanation :
        게임 접속 뷰
        - 캐시에 S3 static data 저장
    """

    lookup_url_kwarg = 'game_id'

    def get_queryset(self):
        return BossRaid.objects.all()

    def get_serializer_class(self):
        return BossRaidSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        url = requests.get(
            "https://dmpilf5svl7rv.cloudfront.net/assignment/backend/bossRaidData.json"
        )

        if url.raise_for_status():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        url.encoding = "utf-8"
        cache.get_or_set("score_data", url)

        res = {
            "Boss Raid": response.data,
        }

        return Response(res, status=status.HTTP_200_OK)


class BossRaidStartAPI(viewsets.GenericViewSet):
    """
    author : 이승민
    request : Dict
    response : Dict, status code
    explanation :
        보스 레이드 시작 뷰
    """

    def get_queryset(self):
        return BossRaidStatus.objects.all()

    def get_serializer_class(self):
        return BossRaidStartSerializer

    @action(detail=False, methods=["post"])
    def enter(self, request):
        """
        보스 레이드 시작 API
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class BossRaidEndAPI(viewsets.GenericViewSet):
    """
    author : 이승민
    request : Dict
    response : Dict, status code
    explanation :
        보스 레이드 종료 뷰
    """

    def get_queryset(self):
        return BossRaidStatus

    def get_serializer_class(self):
        return BossRaidEndSerializer

    @action(detail=False, methods=["patch"])
    def end(self, request):
        """
        보스 레이드 종료 API
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class BossRaidStatusAPI(APIView):
    """
    보스 레이드 status 뷰
    """

    def get(self, request):
        try:
            bossraid_status = BossRaidStatus.objects.all()
            serializer = BossRaidStatusSerializer(bossraid_status, many=True)

            result = []
            for info in serializer.data:
                result.append(
                    {
                        "bossRaidId": info["boss_raid_id"],
                        "canEnter": BossRaid.objects.filter(
                            id=info["boss_raid_id"]
                        ).values("is_entered")[0]["is_entered"],
                        "enteredUserId": info["user_id"],
                    }
                )
            return Response({"status": result}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


class BossRaidRankingAPI(APIView):
    """
    author : 전재완
    explanation : 보스레이드 랭킹 조회 API
    """

    def get(self, request):
        """
        author : 전재완
        param : Request
        return : Response(200/400)
        explanation : list of dictionary 형식의 전체 유저의 보스레이드 랭킹과 점수, dictionary 형의 요청받은 유저의 보스레이드 랭킹과 점수를 포함하는 Response 반환
        """

        try:
            user_id = request.GET.get("userId")
            if user_id:
                user_id = int(user_id)
                ranking_list = RankingDataService.get_ranking_data()
                user_ranking = RankingDataService.get_user_ranking_data(
                    request.GET.get("userId")
                )
                res = {"topRankerInfoList": ranking_list, "myRankingInfo": user_ranking}
                return Response(res, status=status.HTTP_200_OK)
            return Response(
                {"message": "유효하지 않은 user ID 입니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
