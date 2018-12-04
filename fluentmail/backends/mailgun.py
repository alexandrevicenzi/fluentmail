# -*- coding: utf-8 -*-

__all__ = ['Mailgun']

from base64 import b64decode
from quopri import decodestring as decode_quopri

from fluentmail.utils import sanitize_address_list, sanitize_address
from . import base


class Mailgun(base.BaseBackend):

    def __init__(self, account, api_key):
        self.account = account
        self.api_key = api_key

    def _build_data(self, message):
        email_data = {
            'to': sanitize_address_list(message.to),
            'cc': sanitize_address_list(message.cc),
            'bcc': sanitize_address_list(message.bcc),
            'from': sanitize_address(message.from_address),
            'subject': message.subject,
        }

        email_data['text'] = message.body
        email_data['html'] = message.html

        return email_data

    def _build_attachments(self, message):
        attachments = []

        for attachment in message.attachments:
            file_name = attachment.get_filename()
            encoding = attachment.get('Content-Transfer-Encoding', None)

            if encoding == 'base64':
                decode = not attachment.get_content_maintype() in ['audio', 'image', 'text']
                content = b64decode(attachment.get_payload(decode=decode))
            elif encoding == 'quoted-printable':
                content = decode_quopri(attachment.get_payload())
            else:
                content = attachment.get_payload()

            content_type = attachment.get_content_type()
            attachments.append(('attachment', (file_name, content, content_type)))

        return attachments

    def send_multiple(self, messages):
        if self.account and self.api_key:
            import requests

            for message in messages:
                requests.post(
                    'https://api.mailgun.net/v3/%s/messages' % self.account,
                    auth=('api', self.api_key),
                    data=self._build_data(message),
                    files=self._build_attachments(message),
                ).raise_for_status()
