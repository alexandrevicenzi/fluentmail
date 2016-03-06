# -*- coding: utf-8 -*-

from fluentmail.backends import SMTP
from fluentmail import EMailMessage, SSL, TLS


GMAIL_USER = 'user'
GMAIL_PWD = 'password'
FROM = 'sender@gmail.com'
TO = 'receiver@gmail.com'


def send_ssl():
    with SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=SSL) as backend:
        msg = EMailMessage('FluentMail SSL', 'The tiny library to send emails',
                           from_address=FROM, to=TO)
        msg.send(backend)


def send_tls():
    with SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=TLS) as backend:
        msg = EMailMessage('FluentMail TLS', 'The tiny library to send emails',
                           from_address=FROM, to=TO)
        msg.send(backend)


def send_html():
    with SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=TLS) as backend:
        msg = EMailMessage('FluentMail HTML', '<b>The tiny library to send emails<b>', html=True,
                           from_address=FROM, to=TO)
        msg.send(backend)


def send_multiple():
    with SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=TLS) as backend:
        msg1 = EMailMessage('FluentMail Multiple 1', 'The tiny library to send emails',
                            from_address=FROM, to=TO)
        msg2 = EMailMessage('FluentMail Multiple 2', 'The tiny library to send emails',
                            from_address=FROM, to=TO)
        backend.send_multiple([msg1, msg2])


def send_without_with():
    backend = SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=TLS)
    msg = EMailMessage('FluentMail Without With Block', 'The tiny library to send emails',
                       from_address=FROM, to=TO)
    backend.send(msg)


def send_with_encoding():
    backend = SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=TLS)
    msg = EMailMessage('FluentMail com Acentuação', u'Acentuação é um negócio do Português', encoding='iso-8859-1',
                       from_address='FluentMail com Acentuação <%s>' % FROM, to=TO)
    backend.send(msg)


if __name__ == '__main__':
    send_ssl()
    send_tls()
    send_html()
    send_multiple()
    send_without_with()
    send_with_encoding()
