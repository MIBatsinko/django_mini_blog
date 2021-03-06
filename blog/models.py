from django.db import models
from django.contrib.auth.models import User

from article.models import Article


class RatingStar(models.Model):
    """Rating star"""
    value = models.SmallIntegerField("Value", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        ordering = ["-value"]


class Rating(models.Model):
    """Rating"""
    ip = models.CharField("IP address", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="start")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="article", related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.star} - {self.article}"
