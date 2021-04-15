from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.template.loader import get_template

from miniblog.celery import celery_app
from miniblog.settings import EMAIL_HOST_USER


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
