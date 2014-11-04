#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import mimetypes
import os
import smtplib

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

NON_ENCRYPTED = 'AUTH'
SSL = 'SSL'
TLS = 'StartTLS'

EHLO = 'EHLO'
HELO = 'HELO'

MAIL_LIST_SEPARETOR = ', '

class FluentMail:

    def __init__(self, host, port=None, security=NON_ENCRYPTED, verb=EHLO):
        self._host = host
        self._security = security

        if port is None:
            if self._security == SSL:
                self._port = 465
            elif self._security == TLS:
                self._port = 587
            else:
                self._port = 25
        else:
            self._port = port

        self._verb = verb

        self._from_address = None
        self._reply_to = []
        self._to = []
        self._cc = []
        self._bcc = []
        self._subject = None
        self._body = { 'text': None, 'charset': 'utf-8', 'html': False }
        self._attachments = []

        self._credentials = None

    def __append_addresses(self, old, new):
        t = type(new)
        if t == list:
            old += new
        elif t == str:
            old.append(new)
        else:
            raise TypeError('Invalid address type: %s' % new.__class__.__name__)

    def __append_attachments(self, msg):
        # https://docs.python.org/2/library/email-examples.html

        for f in self._attachments:
            filename = f[0]
            charset = f[1]

            if not os.path.isfile(filename):
                continue

            ctype, encoding = mimetypes.guess_type(filename)

            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'

            maintype, subtype = ctype.split('/', 1)

            if maintype == 'text':
                if charset:
                    with codecs.open(filename, 'r', charset) as f:
                        mime = MIMEText(f.read(), _subtype=subtype, _charset=charset)
                else:
                    with open(filename) as f:
                        mime = MIMEText(f.read(), _subtype=subtype)
            elif maintype == 'image':
                with open(filename, 'rb') as f:
                    mime = MIMEImage(f.read(), _subtype=subtype)
            elif maintype == 'audio':
                with open(filename, 'rb') as f:
                    mime = MIMEAudio(f.read(), _subtype=subtype)
            else:
                with open(filename, 'rb') as f:
                    mime = MIMEBase(maintype, subtype)
                    mime.set_payload(f.read())

                encoders.encode_base64(mime)

            mime.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(mime)

    def __build_msg(self):
        msg = MIMEMultipart()

        if not self._from_address:
            raise ValueError('From cannot be empty.')

        msg['From'] = self._from_address

        if not (self._to or self._cc or self._bcc):
            raise ValueError('You must include at least one address at To, Cc or Bcc.')

        if self._to:
            msg['To'] = self.__to_str(self._to)
        if self._cc:
            msg['Cc'] = self.__to_str(self._cc)
        if self._bcc:
            msg['Bcc'] = self.__to_str(self._bcc)
        if self._reply_to:
            msg['Reply-To'] = self.__to_str(self._reply_to)

        msg['Subject'] = self._subject

        if self._body['text']:
            subtype = 'html' if self._body['html'] else 'plain'
            msg.attach(MIMEText(self._body['text'], subtype, self._body['charset']))

        self.__append_attachments(msg)

        return msg.as_string()

    def __to_str(self, l):
        return MAIL_LIST_SEPARETOR.join(l)

    def as_html(self, is_html=True):
        self._body['html'] = is_html
        return self

    def attach(self, filename, charset=None):
        self._attachments.append((filename, charset))
        return self

    def body(self, body, charset='utf-8',):
        self._body['text'] = body
        self._body['charset'] = charset
        return self

    def credentials(self, user, pwd):
        self._credentials = { 'user': user, 'pwd': pwd }
        return self

    def from_address(self, addr):
        self._from_address = addr
        return self

    def to(self, addr):
        self.__append_addresses(self._to, addr)
        return self

    def cc(self, addr):
        self.__append_addresses(self._cc, addr)
        return self

    def bcc(self, addr):
        self.__append_addresses(self._bcc, addr)
        return self

    def reply_to(self, addr):
        self.__append_addresses(self._reply_to, addr)
        return self

    def subject(self, subject):
        self._subject = subject
        return self

    def raw_message(self):
        return self.__build_msg()

    def send(self):
        if self._security == TLS:
            server = smtplib.SMTP(self._host, self._port)
            server.starttls()
        elif self._security == SSL:
            server = smtplib.SMTP_SSL(self._host, self._port)
        else:
            server = smtplib.SMTP(self._host, self._port)

        if self._credentials:
            server.login(self._credentials['user'], self._credentials['pwd'])
        elif self._verb == EHLO:
            server.ehlo()
        elif self._verb == HELO:
            server.helo()

        text = self.__build_msg()
        server.sendmail(self._from_address, self._to, text)
        server.quit()

        return self