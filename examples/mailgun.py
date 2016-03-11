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
        msg = EMailMessage('FluentMail Mailgun HTML', html='<b>Python SMTP client and Email for Humans&#8482;<b>',
                           from_address=FROM, to=TO)
        msg.send(backend)


def send_attachment():
    with Mailgun(ACCOUNT, KEY) as backend:
        msg = EMailMessage('FluentMail Mailgun Attachment', 'Python SMTP client and Email for Humans™',
                           from_address=FROM, to=TO)
        msg.attach('this-is-not-a-file.txt', 'This is not a real file.', 'text/plain')
        msg.attach('pt-BR-encoded.txt', u'Acentuação é um negócio do Português.', 'text/plain', 'iso-8859-1')
        msg.attach_file('./examples/attachments/example.pdf')
        msg.attach_file('./examples/attachments/python-logo.png')
        msg.attach_file('./examples/attachments/encoded-file.txt', encoding='iso-8859-1')
        msg.send(backend)


if __name__ == '__main__':
    send_plain()
    send_html()
    send_attachment()
