from django.apps import AppConfig


class BossraidConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bossRaid"

    def ready(self):
        """
        author : 전재완
        explanation : 입력 받은 user_id에 해당하는 유저의 랭킹과 total score를 dictionary로 반환
        """

        from user.models import TotalScore
        from django.forms.models import model_to_dict
        from django.core.cache import cache
        from collections import defaultdict
        import requests
        import json

        # 전체 랭킹 데이터 캐시 저장
        ranking_scores = TotalScore.objects.all()
        ranking_score_dict = defaultdict(set)

        for ranking_score in ranking_scores:
            ranking_score = model_to_dict(ranking_score)
            ranking_score_dict[ranking_score["total_score"]].add(
                (ranking_score["user"])
            )
        cache.set("ranking_dict", ranking_score_dict, timeout=None)

        # static data 캐시 저장
        static_data = requests.get(
            "https://dmpilf5svl7rv.cloudfront.net/assignment/backend/bossRaidData.json"
        ).json()
        cache.set("bossRaids", static_data)
