from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
import datetime

from bossRaid.models import (
    BossRaidHistory,
    BossRaidStatus,
    BossRaid,
)
from user.models import User


class BossRaidStartSerializer(serializers.Serializer):
    """
    보스 레이드 시작 시리얼라이저
    """

    user = serializers.IntegerField(write_only=True)
    level = serializers.IntegerField(write_only=True)
    boss_raid = serializers.IntegerField(write_only=True)
    isEntered = serializers.SerializerMethodField(read_only=True)
    raidRecordId = serializers.SerializerMethodField(read_only=True)

    def get_isEntered(self, obj):
        return obj.boss_raid.is_entered

    def get_raidRecordId(self, obj):
        return obj.id

    def validate_user(self, user):
        """
        유저에 대한 유효성 검사
        """
        if not user:
            """
            request user가 빈 칸일 때,
            """
            raise serializers.ValidationError(
                _('User ID field not allowed empty')
            )

        get_user = User.objects.filter(id=user)
        if not get_user:
            """
            request user가 존재하지 않을 때,
            """
            raise serializers.ValidationError(
                _('User ID does not exist')
            )

        get_user_raid = BossRaidStatus.objects.filter(user_id=user)
        if get_user_raid.exists():
            """
            request user가 이미 보스 레이드를 진행중 일 때
            """
            raise serializers.ValidationError(
                _('User is already Play Boss Raid !')
            )

        return user

    def validate_level(self, level):
        """
        request level 유효성 검사
        """
        if not level:
            """
            level을 입력하지 않았을 떄,
            """
            raise serializers.ValidationError(
                _('Level field not allowed empty')
            )

        return level

    def validate_boss_raid(self, boss_raid):
        if not boss_raid:
            raise serializers.ValidationError(
                _('Boss Raid field not allowed empty')
            )
        return boss_raid

    def validate(self, data):
        data['user'] = self.validate_user(data['user'])
        data['level'] = self.validate_level(data['level'])
        data['boss_raid'] = self.validate_boss_raid(data['boss_raid'])
        return data

    def create(self, validate_data):
        status = BossRaidStatus.objects.create(
            level=validate_data['level'],
            user_id=validate_data['user'],
            boss_raid_id=validate_data['boss_raid']
        )
        BossRaid.objects.filter(id=validate_data['boss_raid']).update(is_entered=False)
        return status


class BossRaidEndSerializer(serializers.Serializer):
    userId = serializers.IntegerField(write_only=True)
    raidRecordId = serializers.IntegerField(write_only=True)
    boss_raid = serializers.IntegerField(write_only=True)

    def get_userId(self, obj):
        return obj.user

    def get_raidRecordId(self, obj):
        return obj.id

    def validate_userId(self, userId):
        if not userId:
            """
            request user가 빈 칸일 때,
            """
            raise serializers.ValidationError(
                _('User ID field not allowed empty')
            )

        get_user = User.objects.filter(id=userId)
        if not get_user:
            """
            request user가 존재하지 않을 때,
            """
            raise serializers.ValidationError(
                _('User ID does not exist')
            )

        return userId

    def validate_raidRecordId(self, raidRecoreId):
        if not raidRecoreId:
            raise serializers.ValidationError(
                _('raidRecordId field not allowed empty')
            )

        get_raid = BossRaidStatus.objects.filter(id=raidRecoreId)
        if not get_raid:
            raise serializers.ValidationError(
                _('raidRecordId does not exist')
            )

        return raidRecoreId

    def validate_boss_raid(self, boss_raid):
        if not boss_raid:
            raise serializers.ValidationError(
                _('Boss Raid field not allowed empty')
            )
        return boss_raid

    def validate(self, data):
        data['user'] = self.validate_userId(data['userId'])
        data['id'] = self.validate_raidRecordId(data['raidRecordId'])
        data['boss_raid'] = self.validate_boss_raid(data['boss_raid'])
        return data

    def create(self, validate_data):
        get_level = BossRaidStatus.objects.filter(id=validate_data['raidRecordId']).values('level')[0]['level']
        if get_level == 1:
            score = 20
        elif get_level == 2:
            score = 47
        else:
            score = 85
        print(get_level, score)
        status_history = BossRaidHistory.objects.create(
            level=get_level,
            score=score,
            user_id=validate_data['userId'],
            boss_raid_id=validate_data['boss_raid']
        )
        BossRaidStatus.objects.filter(id=validate_data['raidRecordId']).delete()
        BossRaid.objects.filter(id=validate_data['boss_raid']).update(is_entered=True)
        return status_history



