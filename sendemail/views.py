from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import get_template

from .forms import ContactForm
from miniblog.settings import RECIPIENTS_EMAIL, DEFAULT_FROM_EMAIL


class SendingEmail:
    from_email = DEFAULT_FROM_EMAIL
    to_email = RECIPIENTS_EMAIL

    def new_comment(self):
        data = dict()
        subject = 'New comment'
        data['article'] = 1
        data['comment'] = 2
        data['author'] = 3
        message = get_template('sendemail/email.html').render(data)

        msg = EmailMessage(subject, message, from_email=self.from_email, to=self.to_email)
        msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'
        msg.send()
        print('Email was send!')


def contact_view(request):
    # если метод GET, вернем форму
    if request.method == 'GET':
        form = ContactForm()
    elif request.method == 'POST':
        # если метод POST, проверим форму и отправим письмо
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(f'{subject} от {from_email}', message,
                          DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL)
            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма.')
            return redirect('success')
    else:
        return HttpResponse('Неверный запрос.')
    return render(request, "sendemail/email.html", {'form': form})


def success_view(request):
    return HttpResponse('Приняли! Спасибо за вашу заявку.')
