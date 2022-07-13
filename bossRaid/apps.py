from django.apps import AppConfig


class BossraidConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bossRaid'
    
    def ready(self):
        from user.models import TotalScore
        from django.forms.models import model_to_dict
        from django.core.cache import cache
        ranking_scores = TotalScore.objects.all()
        ranking_score_list = []
        for ranking_score in ranking_scores:
            ranking_score_list.append(model_to_dict(ranking_score))
        ranking_score_list.sort(key=lambda x:(x['rank']))
        cache.set('ranking_list', ranking_score_list)