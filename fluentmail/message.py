# -*- coding: utf-8 -*-

__all__ = ['EMailMessage']

import codecs
import os
import mimetypes

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid, formatdate

from .utils import join_address_list, sanitize_address, text_type, string_type

DEFAULT_MIMETYPE = 'application/octet-stream'


class EMailMessage(object):

    def __init__(self, subject='', body='', html=False, encoding=None,
                 from_address=None, to=None, cc=None, bcc=None,
                 reply_to=None, attachments=None):
        self.subject = subject
        self.body = body
        self.from_address = from_address
        self.reply_to = reply_to
        self.attachments = attachments or []
        self.is_html = html
        self.encoding = encoding

        if isinstance(to, (text_type, string_type)):
            self.to = [to]
        elif to:
            self.to = list(to)
        else:
            self.to = []

        if isinstance(cc, (text_type, string_type)):
            self.cc = [cc]
        elif cc:
            self.cc = list(cc)
        else:
            self.cc = []

        if isinstance(bcc, (text_type, string_type)):
            self.bcc = [bcc]
        elif bcc:
            self.bcc = list(bcc)
        else:
            self.bcc = []

    def message(self):
        msg = MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = sanitize_address(self.from_address)
        msg['Date'] = formatdate()
        msg['Message-ID'] = make_msgid()

        if self.to:
            msg['To'] = join_address_list(self.to)

        if self.cc:
            msg['Cc'] = join_address_list(self.cc)

        if self.bcc:
            msg['Bcc'] = join_address_list(self.bcc)

        if self.reply_to:
            msg['Reply-To'] = sanitize_address(self.reply_to)

        if self.body:
            content_subtype = 'html' if self.is_html else 'plain'
            encoding = self.encoding or 'utf-8'
            msg.attach(MIMEText(self.body, content_subtype, encoding))

        for attachment in self.attachments:
            msg.attach(attachment)

        return msg

    def recipients(self):
        return self.to + self.cc + self.bcc

    def raw(self):
        return self.message().as_string()

    def send(self, backend):
        backend.send(self)

    def attach(self, filename, content, mimetype, encoding='utf-8'):
        maintype, subtype = mimetype.split('/', 1)

        if maintype == 'text':
            mime = MIMEText(content, subtype, encoding)
        elif maintype == 'image':
            mime = MIMEImage(content, subtype)
        elif maintype == 'audio':
            mime = MIMEAudio(content, subtype)
        else:
            mime = MIMEBase(maintype, subtype)
            mime.set_payload(content, encoding)
            encoders.encode_base64(mime)

        self.attach_mime(filename, mime)

    def attach_mime(self, filename, mime):
        if not isinstance(mime, MIMEBase):
            raise TypeError('"mime" must be an instance of MIMEBase.')

        if filename:
            try:
                filename.encode('ascii')
            except UnicodeEncodeError:
                filename = ('utf-8', '', filename)

            mime.add_header('Content-Disposition', 'attachment', filename=filename)

        self.attachments.append(mime)

    def attach_file(self, path, mimetype=None, encoding=None):
        content = None
        filename = os.path.basename(path)

        if not mimetype:
            mimetype, _ = mimetypes.guess_type(filename)

            if not mimetype:
                mimetype = DEFAULT_MIMETYPE

        if encoding:
            with codecs.open(path, 'rb', encoding) as f:
                content = f.read()
        else:
            with open(path, 'rb') as f:
                content = f.read()

        self.attach(filename, content, mimetype)
