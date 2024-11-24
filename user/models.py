from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

class staffTrack(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length = 80, blank=True)
    todays_date = models.DateTimeField(blank=True)
    login_time = models.DateTimeField(blank=True)
    logout_time = models.DateTimeField(blank=True, null=True)



class staffVacation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    vacationTime = models.IntegerField(default=15)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:

        staffVacation.objects.create(user = instance)


class staffLate(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todays_date = models.DateTimeField(blank=True)
    late_diff = models.CharField(max_length= 200, blank=True)


