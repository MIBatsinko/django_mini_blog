import os

from django.db import models
from django.contrib.auth.models import User


# def avatar_upload_to(instance, filename):
#     return os.path.join('uploads', instance.user.username + os.path.splitext(filename)[1])


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="/profile1.png", null=True, blank=True)  # upload_to='images/',
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    #  user = models.ForeignKey(User, unique=True)

    def __str__(self):
        return self.user.username
