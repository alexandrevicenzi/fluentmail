# -*- coding: utf-8 -*-

from fluentmail.backends import SMTP
from fluentmail import EMailMessage, SSL, TLS


GMAIL_USER = 'user'
GMAIL_PWD = 'password'
FROM = 'sender@gmail.com'
TO = 'receiver@gmail.com'


def send_ssl():
    with SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=SSL) as backend:
        msg = EMailMessage('FluentMail SSL', 'Python SMTP client and Email for Humans™',
                           from_address=FROM, to=TO)
        msg.send(backend)


def send_tls():
    with SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=TLS) as backend:
        msg = EMailMessage('FluentMail TLS', 'Python SMTP client and Email for Humans™',
                           from_address=FROM, to=TO)
        msg.send(backend)


def send_html():
    with SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=TLS) as backend:
        msg = EMailMessage('FluentMail HTML', html='<b>Python SMTP client and Email for Humans&#8482;<b>',
                           from_address=FROM, to=TO)
        msg.send(backend)


def send_multiple():
    with SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=TLS) as backend:
        msg1 = EMailMessage('FluentMail Multiple 1', 'Python SMTP client and Email for Humans™',
                            from_address=FROM, to=TO)
        msg2 = EMailMessage('FluentMail Multiple 2', 'Python SMTP client and Email for Humans™',
                            from_address=FROM, to=TO)
        backend.send_multiple([msg1, msg2])


def send_without_with():
    backend = SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=TLS)
    msg = EMailMessage('FluentMail Without With Block', 'Python SMTP client and Email for Humans™',
                       from_address=FROM, to=TO)
    backend.send(msg)


def send_with_encoding():
    backend = SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=TLS)
    msg = EMailMessage('FluentMail com Acentuação', u'Acentuação é um negócio do Português', encoding='iso-8859-1',
                       from_address='FluentMail com Acentuação <%s>' % FROM, to=TO)
    backend.send(msg)


def send_attachment():
    with SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=TLS) as backend:
        msg = EMailMessage('FluentMail Attachment', 'Python SMTP client and Email for Humans™',
                           from_address=FROM, to=TO)
        msg.attach('this-is-not-a-file.txt', 'This is not a real file.', 'text/plain')
        msg.attach('pt-BR-encoded.txt', u'Acentuação é um negócio do Português.', 'text/plain', 'iso-8859-1')
        msg.attach_file('./examples/attachments/example.pdf')
        msg.attach_file('./examples/attachments/python-logo.png')
        msg.attach_file('./examples/attachments/encoded-file.txt', encoding='iso-8859-1')
        msg.send(backend)


if __name__ == '__main__':
    send_ssl()
    send_tls()
    send_html()
    send_multiple()
    send_without_with()
    send_with_encoding()
    send_attachment()
