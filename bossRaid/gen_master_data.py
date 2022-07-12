from bossRaid.models import (
    BossRaidHistory,
    BossRaidStatus,
    BossRaid
)
from user.models import User


def gen_master(apps, schema_editor):
    user = User(
        id=1,
        username='user1',
        password='user1'
    )
    user.save()

    boss = BossRaid(
        name='닌자대전'
    )
    boss.save()

    history = BossRaidHistory(
        level=1,
        score=20,
        user=1,
        boss_raid=boss.id
    )
    history.save()

    status = BossRaidStatus(
        level=1,
        is_entered=False,
        user=1,
        boss_raid=boss.id
    )
    status.save()
