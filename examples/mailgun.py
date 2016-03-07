# -*- coding: utf-8 -*-

from fluentmail.backends import Mailgun
from fluentmail import EMailMessage

ACCOUNT = 'yourdomain.com'
KEY = 'key-767236467251631563'
FROM = 'sender@yourdomain.com'
TO = 'receiver@fluentmail.com'


def send_plain():
    with Mailgun(ACCOUNT, KEY) as backend:
        msg = EMailMessage('FluentMail Mailgun', 'Python SMTP client and Email for Humans™',
                           from_address=FROM, to=TO)
        msg.send(backend)


def send_html():
    with Mailgun(ACCOUNT, KEY) as backend:
        msg = EMailMessage('FluentMail Mailgun HTML', '<b>Python SMTP client and Email for Humans&#8482;<b>',
                           from_address=FROM, to=TO, html=True)
        msg.send(backend)


if __name__ == '__main__':
    send_plain()
    send_html()
