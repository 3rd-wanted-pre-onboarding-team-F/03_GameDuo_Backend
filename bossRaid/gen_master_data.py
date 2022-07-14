from bossRaid.models import (
    BossRaidHistory,
    BossRaidStatus,
    BossRaid
)
from user.models import User


def gen_master(apps, schema_editor):
    boss = BossRaid(
        name='닌자대전'
    )
    boss.save()
