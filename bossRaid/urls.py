from django.urls import path

from bossRaid.views import (
    BossRaidStartAPI,
    BossRaidEndAPI,
    BossRaidStatusAPI,
    BossRaidRankingAPI,
    BossRaidAPI,
)

boss_raid = BossRaidAPI.as_view({
    'get': 'retrieve'
})
raid_start = BossRaidStartAPI.as_view({
    'post': 'enter'
})
raid_end = BossRaidEndAPI.as_view({
    'patch': "end"
})


urlpatterns = [
    path('<int:game_id>/', boss_raid),
    path('enter/', raid_start),
    path('end/', raid_end),
    path('bossRaid/', BossRaidStatusAPI.as_view()),
    path('topRankerList/', BossRaidRankingAPI.as_view()),
]