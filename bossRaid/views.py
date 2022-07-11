from django.shortcuts import render
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from bossRaid.serializers import (
    BossRaidStartSerializer
)
from bossRaid.models import (
    BossRaidHistory,
    BossRaidStatus,
    BossRaid
)
from user.models import User


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





