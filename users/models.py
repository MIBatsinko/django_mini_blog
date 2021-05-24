from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="/avatar.png", null=True, blank=True)  # upload_to='images/',
    date_created = models.DateTimeField(auto_now_add=True)
    total_rating = models.FloatField(default=0)

    def __str__(self):
        return self.user.username
