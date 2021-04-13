from django.db import models
from django.urls import reverse

from article.models import Article
from django.contrib.auth.models import User


class Comment(models.Model):
    body = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):  # new
        return reverse('blog_view', args=[str(self.id)])

    def __str__(self):
        return f"Comment {self.id}: from the {self.author} on the {self.article}"
