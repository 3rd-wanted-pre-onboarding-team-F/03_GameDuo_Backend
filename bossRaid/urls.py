from django.urls import path

from bossRaid.views import (
    BossRaidStartAPI
)

raid_start = BossRaidStartAPI.as_view({
    'post': 'enter'
})


urlpatterns = [
    path('enter/', raid_start),
]