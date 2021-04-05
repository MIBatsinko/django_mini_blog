from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import get_template

from article.models import Article
from .forms import ContactForm
from miniblog.settings import EMAIL_HOST_USER


class SendingEmail:
    from_email = EMAIL_HOST_USER

    def new_comment(self, article, author, comment):
        data = dict()
        data['article'] = article.title
        data['comment'] = comment
        data['author'] = author.username
        data['url'] = ''  # url of article
        subject = 'New comment to the {}'.format(data['article'])
        message = get_template('sendemail/email.html').render(data)

        self.to_email = [article.author.email]  # delete
        msg = EmailMessage(subject, message, from_email=self.from_email, to=self.to_email)
        msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'
        msg.send()
        print('Email was send to {}!'.format(self.to_email))
