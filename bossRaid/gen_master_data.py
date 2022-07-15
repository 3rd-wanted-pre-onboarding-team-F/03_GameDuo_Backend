from bossRaid.models import (
    BossRaidHistory,
    BossRaidStatus,
    BossRaid
)


def gen_master(apps, schema_editor):
    """
    author : 이승민
    explanation :
        보스 레이드 게임 더미데이터
    """
    boss = BossRaid(
        name='닌자대전'
    )
    boss.save()
