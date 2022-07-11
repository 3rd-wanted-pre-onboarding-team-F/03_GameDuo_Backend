from django.db import models


# Create your models here.
class BossRaidHistory(models.Model):
    level = models.PositiveIntegerField('레벨')
    score = models.PositiveIntegerField('점수', default=0)
    enter_time = models.DateTimeField('입장 시간', auto_now_add=True)
    end_time = models.DateTimeField('퇴장 시간')

    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_boss_history'
        ordering = ('-id',)
        verbose_name = '보스 레이드 기록'
        verbose_name_plural = '보스 레이드 기록들'

    def __str__(self):
        return f'{self.id}, level = {self.level}, score = {self.score}'


class BossRaidStatus(models.Model):
    level = models.PositiveIntegerField('레벨')
    is_entered = models.BooleanField('입장 여부', default=False)
    last_entertime = models.DateTimeField('마지막 입장 시간')

    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_boss_status'
        ordering = ('-id',)
        verbose_name = '보스 레이드 상태'
        verbose_name_plural = '보스 레이드 상태들'

    def __str__(self):
        return f'{self.id}, level = {self.level}, CanEntered = {self.is_entered}'




