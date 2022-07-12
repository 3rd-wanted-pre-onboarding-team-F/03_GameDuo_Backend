from django.urls import path

from bossRaid.views import (
    BossRaidStartAPI,
    BossRaidEndAPI,
    BossRaidStatusAPI
)

raid_start = BossRaidStartAPI.as_view({
    'post': 'enter'
})
raid_end = BossRaidEndAPI.as_view({
    'patch': "end"
})


urlpatterns = [
    path('enter/', raid_start),
    path('end/', raid_end),
    path('bossRaid/', BossRaidStatusAPI.as_view())
]