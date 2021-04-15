from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.template.loader import get_template

from miniblog.celery import celery_app
from miniblog.settings import EMAIL_HOST_USER

from django.conf import settings
from django.core.mail import send_mail
from django.template import Engine, Context
from celery import shared_task


@shared_task
def adding_task(x, y):
    return x + y


def render_template(template, context):
    engine = Engine.get_default()

    tmpl = engine.get_template(template)

    return tmpl.render(Context(context))


@celery_app.task
def send_mail_task(recipients, subject, template, context):
    send_mail(
        subject=subject,
        message=render_template(f'{template}.txt', context),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
        fail_silently=False,
        html_message=render_template(f'{template}.html', context)
    )


@celery_app.task()
def send_email(article, author, comment):
    data = dict()
    data['article'] = article
    data['comment'] = comment
    data['author'] = author
    data['url'] = ''  # url of article
    subject = 'New comment to the {}'.format(data['article'])
    message = get_template('comment/email.html').render(data)
    from_email = EMAIL_HOST_USER
    to_email = [article.author.email]  # delete
    msg = EmailMessage(subject, message, from_email=from_email, to=to_email)
    msg.content_subtype = 'html'
    msg.mixed_subtype = 'related'
    msg.send()
    print('Email was send to {}!'.format(to_email))

