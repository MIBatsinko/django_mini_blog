# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

APIKEY = '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'


message = Mail(
    from_email='bat',
    to_emails='ЛЮБАЯ ПОЧТА',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(APIKEY)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
