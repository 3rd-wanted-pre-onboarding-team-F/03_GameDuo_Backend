from django.contrib import admin
from bossRaid.models import (
    BossRaidHistory,
    BossRaidStatus,
)


# Register your models here.
admin.site.register(BossRaidHistory)
admin.site.register(BossRaidStatus)

