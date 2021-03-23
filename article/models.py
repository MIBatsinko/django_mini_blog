from django.db import models
from django.urls import reverse


class Author(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def get_absolute_url(self):  # new
        return reverse('blog_view', args=[str(self.id)])

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    body = models.TextField()
    author = models.ForeignKey('Author', related_name='article', on_delete=models.CASCADE)

    def get_absolute_url(self):  # new
        return reverse('blog_view', args=[str(self.id)])

    def __str__(self):
        return self.title
