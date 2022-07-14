from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from threading import Timer
from django.core.cache import cache
from django.db import transaction
from django.db.models import Sum


from bossRaid.models import (
    BossRaidHistory,
    BossRaidStatus,
    BossRaid,
)
from bossRaid.services import (
    StatusService,
    HistoryService,
)
from user.models import User, TotalScore


class BossRaidSerializer(serializers.ModelSerializer):
    """
    게임 접속 시리얼라이저
    """
    class Meta:
        model = BossRaid
        fields = [
            'id', 'name'
        ]


class BossRaidHistorySerializer(serializers.ModelSerializer):
    """
    보스 레이드 히스토리 시리얼라이저
    """

    class Meta:
        model = BossRaidHistory
        fields = [
            'id',
            'score',
            'enter_time',
            'end_time',
        ]


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
        """
        request boss_raid 유효성 검사
        """
        if not boss_raid:
            """ boss_raid를 입력하지 않았을 때 """
            raise serializers.ValidationError(
                _('Boss Raid field not allowed empty')
            )

        get_boss = BossRaid.objects.filter(id=boss_raid)
        if not get_boss.exists():
            """ 보스 레이드가 존재하지 않을 때 """
            raise serializers.ValidationError(
                _('Boss raid does not exist')
            )

        get_boss_id = BossRaid.objects.get(id=boss_raid)
        if get_boss_id.is_entered == False:
            """ 보스레이드가 이미 실행중 일때 """
            raise serializers.ValidationError(
                _('Boss Raid is already Playing')
            )
        return boss_raid

    def validate(self, data):
        data['user'] = self.validate_user(data['user'])
        data['level'] = self.validate_level(data['level'])
        data['boss_raid'] = self.validate_boss_raid(data['boss_raid'])
        return data

    @transaction.atomic()
    def create(self, validate_data):
        """
        Boss Status 데이터 생성
        """
        set_status_create = StatusService()
        status = set_status_create.set_status(validate_data)
        boss_time = cache.get('score_data').json()['bossRaids'][0]['bossRaidLimitSeconds']

        def timer_delete():
            """
            보스 레이드를 시작하고 사용자가 레이드에 실패 했을 때
            타이머 동작 (180초)
            180초 후에 Boss Status가 자동으로 삭제
            """
            if status:
                set_create_timer = StatusService()
                set_create_timer.set_timer(validate_data, status)

        Timer(30, timer_delete).start()

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
        """
        request userId 유효성 검사
        """
        if not userId:
            """ request user가 빈 칸일 때 """
            raise serializers.ValidationError(
                _('User ID field not allowed empty')
            )

        get_user = User.objects.filter(id=userId)
        if not get_user:
            """ request user가 존재하지 않을 때 """
            raise serializers.ValidationError(
                _('User ID does not exist')
            )

        return userId

    def validate_raidRecordId(self, raidRecoreId):
        """
        request raidRecordId 유효성 검사
        """
        if not raidRecoreId:
            """ raidRecordId를 입력하지 않았을 때"""
            raise serializers.ValidationError(
                _('raidRecordId field not allowed empty')
            )

        get_raid = BossRaidStatus.objects.filter(id=raidRecoreId)
        if not get_raid:
            """ 보스 레이드가 이미 실행중 일때"""
            raise serializers.ValidationError(
                _('raidRecordId does not exist')
            )

        return raidRecoreId

    def validate_boss_raid(self, boss_raid):
        """
        request boss_raid 유효성 검사
        """
        if not boss_raid:
            """ boss_raid를 입력하지 않았을 때 """
            raise serializers.ValidationError(
                _('Boss Raid field not allowed empty')
            )
        return boss_raid

    def validate(self, data):
        data['user'] = self.validate_userId(data['userId'])
        data['id'] = self.validate_raidRecordId(data['raidRecordId'])
        data['boss_raid'] = self.validate_boss_raid(data['boss_raid'])
        return data

    @transaction.atomic()
    def create(self, validate_data):
        """
        보스레이드 종료 시 점수 반환 및 Boss Status 데이터 삭제
        BossRaid의 is_entered 필드의 입장 가능 여부를 True로 수정
        """
        set_create_history = HistoryService()
        history = set_create_history.set_history(validate_data)

        sum = BossRaidHistory.objects.aggregate(Sum('score'))['score__sum']
        user = TotalScore.objects.select_for_update().get(user_id=validate_data['userId'])
        user.total_score = sum
        user.save()

        is_enter = BossRaid.objects.select_for_update().get(id=validate_data['boss_raid'])
        is_enter.is_entered = True
        is_enter.save()
        return history


class BossRaidStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BossRaidStatus
        fields = ('id', 'user_id', 'level', 'boss_raid_id', 'last_entertime')