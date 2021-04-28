from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models, IntegrityError, transaction
from django.dispatch import receiver

from article.models import Article
from blog.models import Rating, UserProfile
from comment.models import Comment


@receiver(post_save, sender=Rating)
def calculate_avg_rating_article(sender, instance, **kwargs):
    rating = sender.objects.filter(article=instance.article).aggregate(models.Avg('star_id'))
    instance.article.total_rating = rating.get('star_id__avg', 0)
    instance.article.save()


@receiver(post_save, sender=Rating)
def calculate_avg_rating_author(sender, instance, **kwargs):
    rating = Article.objects.filter(author_id=instance.article.author).aggregate(models.Avg('total_rating'))
    instance.article.author.userprofile.total_rating = rating.get('total_rating__avg', 0)
    instance.article.author.userprofile.save()


@receiver(post_save, sender=User)
def create_userprofile(sender, instance, **kwargs):
    try:
        # Fixed: django.db.transaction.TransactionManagementError:
        # An error occurred in the current transaction.
        # You can't execute queries until the end of the 'atomic' block.
        with transaction.atomic():
            userprofile = UserProfile.objects.create(user=instance, avatar='/avatar.png')
            userprofile.save()
    except IntegrityError:
        pass
