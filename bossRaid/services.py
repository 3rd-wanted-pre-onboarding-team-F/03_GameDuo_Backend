from django.core.cache import cache

from bossRaid.models import (
    BossRaid,
    BossRaidHistory,
    BossRaidStatus
)


class StatusService(object):
    """
    BossRaidStatus Data 생성
    보스 레이드 시작 API 호출 시, 보스 레이드의 진행 상태와 관련된 DB를 조작하는 Service
    """
    def set_status(self, validate_data):
        """
        보스 레이드 시작 후, 스테이터스 데이터 적재
        """
        status = BossRaidStatus.objects.create(
            level=validate_data['level'],
            user_id=validate_data['user'],
            boss_raid_id=validate_data['boss_raid']
        )
        status.save()
        BossRaid.objects.filter(id=validate_data['boss_raid']).update(is_entered=False)
        return status

    def set_timer(self, validate_data, status):
        """
        보스 레이드 시작 후, 타이머 작동
        타이머 시간 초과가 되면 히스토리 데이터 적재 후, 스테이터스 데이터 삭제
        """
        is_enter = BossRaid.objects.get(id=validate_data['boss_raid'])
        is_enter.is_entered = True
        is_enter.save()
        history = BossRaidHistory.objects.create(
            level=validate_data['level'],
            score=0,
            user_id=validate_data['user'],
            boss_raid_id=validate_data['boss_raid']
        ).save()
        status.delete()

        return history



class HistoryService(object):
    """
    BossRaidHistory
    보스 레이드 종료 API 호출 시, 레벨에 맞는 점수를 반환 및 업데이트를 하고
    BossRaidHistory에 데이터를 적재 후, BossRaidStatus 데이터를 삭제한다.
    """
    def set_history(self, validate_data):
        """
        보스 레이드 종료 후, 점수 계산 및 히스토리 데이터 저장
        """
        get_level = BossRaidStatus.objects.filter(
            id=validate_data['raidRecordId']
        ).values('level')[0]['level']
        level = cache.get('score_data').json()['bossRaids'][0]['levels']

        if get_level - 1 == level[0]['level']:
            score = level[0]['score']
        elif get_level - 1 == level[1]['level']:
            score = level[1]['score']
        elif get_level - 1 == level[2]['level']:
            score = level[2]['score']
        else:
            score = 0

        history = BossRaidHistory.objects.create(
            level=get_level,
            score=score,
            user_id=validate_data['userId'],
            boss_raid_id=validate_data['boss_raid']
        )
        BossRaidStatus.objects.filter(id=validate_data['raidRecordId']).delete()

        return history


