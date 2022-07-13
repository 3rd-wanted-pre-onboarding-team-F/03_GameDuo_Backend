from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    class Meta:
        db_table = 'users'
    
    
class TotalScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_score = models.IntegerField('총 합 점수', default=0)

    class Meta:
        db_table = 'tb_total_score'

    def __str__(self):
        return f'User = {self.user} --- Total Score = {self.total_score}'