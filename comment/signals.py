from django.db.models.signals import post_save
from django.dispatch import receiver

from comment.models import Comment


@receiver(post_save, sender=Comment)
def comment_send_email(sender, instance, **kwargs):
    from .tasks import send_email
    send_email.delay(instance.article.id, instance.author.username, instance.body)
