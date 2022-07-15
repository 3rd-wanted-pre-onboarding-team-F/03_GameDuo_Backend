from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


# Create your models here.


class TotalScore(models.Model):
    """
    author : 임혁, 이승민
    explanation : User별 total_score(총 합 점수) 출력
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.IntegerField("총 합 점수", default=0)

    class Meta:
        db_table = "tb_total_score"

    def __str__(self):
        return f"User = {self.user.username} --- Total Score = {self.total_score}"


@receiver(post_save, sender=User)
def create_user_total_score(sender, instance, created, **kwargs):
    """
    author : 임혁
    explanation : User 인스턴스 생성 시, post 시그널을 받아 TotalScore 인스턴스를 생성하는 함수
    """
    if created:
        TotalScore.objects.create(user=instance)
