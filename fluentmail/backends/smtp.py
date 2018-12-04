# -*- coding: utf-8 -*-

__all__ = ['NON_ENCRYPTED', 'SSL', 'TLS', 'HELO', 'HELO', 'SMTP']

import smtplib

from fluentmail.utils import sanitize_address, join_address_list
from . import base

NON_ENCRYPTED = 'AUTH'
SSL = 'SSL'
TLS = 'StartTLS'

EHLO = 'EHLO'
HELO = 'HELO'


class SMTP(base.BaseBackend):

    def __init__(self, host, port=None, security=NON_ENCRYPTED, verb=EHLO, user=None, password=None):
        self.host = host
        self.security = security
        self.verb = verb
        self.user = user
        self.password = password
        self.connection = None

        if port is None:
            if self.security == SSL:
                self.port = 465
            elif self.security == TLS:
                self.port = 587
            else:
                self.port = 25
        else:
            self.port = port

    def open(self):
        if self.connection:
            return False

        if self.security == TLS:
            self.connection = smtplib.SMTP(self.host, self.port)
            self.connection.starttls()
        elif self.security == SSL:
            self.connection = smtplib.SMTP_SSL(self.host, self.port)
        else:
            self.connection = smtplib.SMTP(self.host, self.port)

        if self.user and self.password:
            self.connection.login(self.user, self.password)
        elif self.verb == EHLO:
            self.connection.ehlo()
        elif self.verb == HELO:
            self.connection.helo()

        return True

    def close(self):
        if self.connection:
            self.connection.quit()
            self.connection = None
            return True
        return False

    def send_multiple(self, messages):
        if not messages:
            return

        new_connection = self.open()

        for message in messages:
            from_address = sanitize_address(message.from_address)
            recipients = join_address_list(message.recipients())
            self.connection.sendmail(from_address, recipients, message.raw_message())

        if new_connection:
            self.close()
