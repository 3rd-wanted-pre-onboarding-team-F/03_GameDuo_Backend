from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User



# Create your models here.

class TotalScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.PositiveIntegerField(default=0)
    
@receiver(post_save, sender=User)
def create_user_total_score(sender, instance, created, **kwargs):
    if created:
        TotalScore.objects.create(user=instance)