from django.contrib import admin
from bossRaid.models import (
    BossRaidHistory,
    BossRaidStatus,
    BossRaid,
)


# Register your models here.
admin.site.register(BossRaid)
admin.site.register(BossRaidHistory)
admin.site.register(BossRaidStatus)
