from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from article.models import Article
from miniblog.celery import celery_app
from django.conf import settings


@celery_app.task()
def send_email(article_id, author_username, comment_body):
    article = Article.objects.get(id=article_id)
    data = {
        'article': article.title,
        'comment': comment_body,
        'author': author_username
    }
    subject = 'New comment to the {}'.format(get_object_or_404(data, 'article'))
    message = get_template('comment/email.html').render(data)
    msg = EmailMessage(subject, message, from_email=settings.EMAIL_HOST_USER, to=[article.author.email])
    msg.content_subtype = 'html'
    msg.mixed_subtype = 'related'
    msg.send()
    print('Email was send to {}!'.format([article.author.email]))
