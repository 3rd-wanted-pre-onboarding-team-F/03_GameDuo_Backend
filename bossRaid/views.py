from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from bossRaid.serializers import (
    BossRaidStartSerializer,
    BossRaidEndSerializer, BossRaidStatusSerializer,
)
from bossRaid.models import (
    BossRaidHistory,
    BossRaidStatus,
    BossRaid
)


class BossRaidStartAPI(viewsets.GenericViewSet):
    """
    보스 레이드 시작 뷰
    """

    def get_queryset(self):
        return BossRaidStatus.objects.all()

    def get_serializer_class(self):
        return BossRaidStartSerializer

    @action(detail=False, methods=['post'])
    def enter(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )


class BossRaidEndAPI(viewsets.GenericViewSet):
    """
    보스 레이드 종료 뷰
    """

    def get_queryset(self):
        return BossRaidStatus

    def get_serializer_class(self):
        return BossRaidEndSerializer

    @action(detail=False, methods=['patch'])
    def end(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )


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
                result.append({
                    'bossRaidId': info['boss_raid_id'],
                    'canEnter': BossRaid.objects.filter(id=info['boss_raid_id']).values('is_entered')[0]['is_entered'],
                    'enteredUserId': info['user_id']
                })
            return Response({
                "status": result
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": f"{e}"
            }, status=status.HTTP_400_BAD_REQUEST)