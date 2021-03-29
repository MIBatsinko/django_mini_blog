from django.db import models
from django.contrib.auth.models import User

from article.models import Article


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="/profile1.png", null=True, blank=True)  # upload_to='images/',
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class RatingStar(models.Model):
    """Rating star"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        ordering = ["-value"]


class Rating(models.Model):
    """Rating"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="start")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="article", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.article}"
