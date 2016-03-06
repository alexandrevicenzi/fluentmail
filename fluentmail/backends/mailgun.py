# -*- coding: utf-8 -*-

__all__ = ['Mailgun']

from . import base


class Mailgun(base.BaseBackend):
    def __init__(self, account, api_key):
        self.account = account
        self.api_key = api_key

    def _build_data(self, message):
        email_data = {
            'to': ', '.join(message.to),
            'cc': ', '.join(message.cc),
            'bcc': ', '.join(message.bcc),
            'to': ', '.join(message.to),
            'from': message.from_address,
            'subject': message.subject,
        }

        key = 'html' if message.is_html else 'text'
        email_data[key] = message.body

    def send_multiple(self, messages):
        if self.account and self.api_key:
            import requests

            for message in messages:
                requests.post(
                    'https://api.mailgun.net/v3/%s/messages' % self.account,
                    auth=('api', self.api_key),
                    data=self._build_data(message),
                ).raise_for_status()
