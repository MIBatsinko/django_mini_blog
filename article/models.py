from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.datetime_safe import datetime


class Category(models.Model):
    name = models.CharField("Category", max_length=150)
    description = models.TextField("Description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Article(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    body = models.TextField()
    author = models.ForeignKey(User, related_name='article', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=1)
    date = models.DateTimeField('Date of publication', default=timezone.now)
    total_rating = models.FloatField(default=0)

    def get_absolute_url(self):
        return reverse('blog_view', args=[str(self.id)])

    def __str__(self):
        return self.title
