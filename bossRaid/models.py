from django.db import models

from user.models import User


# Create your models here.
class BossRaid(models.Model):
    name = models.CharField('보스 레이드 이름', max_length=100)
    is_entered = models.BooleanField('입장 여부', default=True)

    class Meta:
        db_table = 'db_boss_raid'
        ordering = ('-id',)
        verbose_name = '보스 레이드'
        verbose_name_plural = '보스 레이드들'

    def __str__(self):
        return f'{self.id}, {self.name} -- is_Entered = {self.is_entered}'


class BossRaidHistory(models.Model):
    level = models.PositiveIntegerField('레벨')
    score = models.PositiveIntegerField('점수', default=0)
    enter_time = models.DateTimeField('입장 시간', auto_now_add=True)
    end_time = models.DateTimeField('퇴장 시간', auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boss_raid = models.ForeignKey(BossRaid, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_boss_history'
        ordering = ('-id',)
        verbose_name = '보스 레이드 기록'
        verbose_name_plural = '보스 레이드 기록들'

    def __str__(self):
        return f'{self.id}, level = {self.level}, score = {self.score} -- Boss Raid = {self.boss_raid}'


class BossRaidStatus(models.Model):
    level = models.PositiveIntegerField('레벨')
    last_entertime = models.DateTimeField('마지막 입장 시간', auto_now_add=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    boss_raid = models.OneToOneField(BossRaid, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_boss_status'
        ordering = ('-id',)
        verbose_name = '보스 레이드 상태'
        verbose_name_plural = '보스 레이드 상태들'

    def __str__(self):
        return f'{self.id}, level = {self.level} -- Boss Raid = {self.boss_raid}'




