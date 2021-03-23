from django.db import models
from django.urls import reverse

from article.models import Article, Author


class Comment(models.Model):
    body = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def get_absolute_url(self):  # new
        return reverse('blog_view', args=[str(self.id)])

    def __str__(self):
        return f"Comment {self.id}: from the {self.author} on the {self.article}"
