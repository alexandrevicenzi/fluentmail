#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from fluentmail import Message, DEFAULT_MIMETYPE
from fluentmail.utils import sanitize_address, sanitize_address_list, join_address_list, PY3


class TestMessage(unittest.TestCase):

    def test_body_plain(self):
        msg = Message('FluentMail', 'Python SMTP client and Email for Humans™')
        mime = msg.mime_message()
        body = mime.get_payload()[0]
        self.assertEqual(body.get_content_type(), 'text/plain')
        self.assertEqual(body.get_charset(), 'utf-8')
        self.assertEqual(body.get_payload(), 'UHl0aG9uIFNNVFAgY2xpZW50IGFuZCBFbWFpbCBmb3IgSHVtYW5z4oSi\n')

    def test_body_plain_russian(self):
        msg = Message('FluentMail', u'К сожалению, мы должны сообщить')
        mime = msg.mime_message()
        body = mime.get_payload()[0]
        self.assertEqual(body.get_content_type(), 'text/plain')
        self.assertEqual(body.get_charset(), 'utf-8')
        self.assertEqual(body.get_payload(), '0Jog0YHQvtC20LDQu9C10L3QuNGOLCDQvNGLINC00L7Qu9C20L3RiyDRgdC+0L7QsdGJ0LjRgtGM\n')

    def test_body_plain_chinese(self):
        msg = Message('FluentMail', u'我的测试文档')
        mime = msg.mime_message()
        body = mime.get_payload()[0]
        self.assertEqual(body.get_content_type(), 'text/plain')
        self.assertEqual(body.get_charset(), 'utf-8')
        self.assertEqual(body.get_payload(), '5oiR55qE5rWL6K+V5paH5qGj\n')

    def test_body_html(self):
        msg = Message('FluentMail', html='<b>Python SMTP client and Email for Humans&#8482;<b>')
        mime = msg.mime_message()
        body = mime.get_payload()[0]
        self.assertEqual(body.get_content_type(), 'text/html')
        self.assertEqual(body.get_charset(), 'utf-8')
        self.assertEqual(body.get_payload(), 'PGI+UHl0aG9uIFNNVFAgY2xpZW50IGFuZCBFbWFpbCBmb3IgSHVtYW5zJiM4NDgyOzxiPg==\n')

    def test_body_encoding(self):
        msg = Message('FluentMail', u'Acentuação é um negócio do Português', encoding='iso-8859-1')
        mime = msg.mime_message()
        body = mime.get_payload()[0]
        self.assertEqual(body.get_content_type(), 'text/plain')
        self.assertEqual(body.get_charset(), 'iso-8859-1')
        self.assertEqual(body.get_payload(), 'Acentua=E7=E3o =E9 um neg=F3cio do Portugu=EAs')

    def test_alternative_body(self):
        msg = Message('FluentMail', 'Python SMTP client and Email for Humans™', '<b>Python SMTP client and Email for Humans&#8482;<b>')
        mime = msg.mime_message()
        alternative = mime.get_payload()[0]
        self.assertEqual(alternative.get_content_type(), 'multipart/alternative')
        self.assertEqual(alternative.get_charset(), None)
        plain = alternative.get_payload()[0]
        html = alternative.get_payload()[1]
        self.assertEqual(plain.get_content_type(), 'text/plain')
        self.assertEqual(html.get_content_type(), 'text/html')

    def test_attachment(self):
        msg = Message()
        msg.attach('myfile.txt', 'my content', 'text/plain')
        attachment = msg.attachments[0]
        self.assertEqual(attachment.get_content_type(), 'text/plain')
        self.assertEqual(attachment.get_charset(), 'utf-8')
        self.assertEqual(attachment.get_payload(), 'my content')
        self.assertEqual(attachment.get_filename(), 'myfile.txt')
        self.assertEqual(attachment['Content-Disposition'], 'attachment; filename="myfile.txt"')

    def test_attachment_file_encoded(self):
        msg = Message()
        # this file is encoded with iso-8859-1
        msg.attach_file('./tests/encoded-file.txt', 'text/plain')
        attachment = msg.attachments[0]

        # Python 3 fails to open encoded file without binary mode.
        if PY3:
            self.assertEqual(attachment.get_content_type(), DEFAULT_MIMETYPE)
            self.assertEqual(attachment.get_payload(), 'QWNlbnR1YefjbyDpIHVtIG5lZ/NjaW8gZG8gUG9ydHVndepz\n')
        else:
            self.assertEqual(attachment.get_content_type(), 'text/plain')
            self.assertEqual(attachment.get_charset(), 'utf-8')
            self.assertEqual(attachment.get_payload(), u'Acentuação é um negócio do Português'.encode('iso-8859-1'))

        self.assertEqual(attachment.get_filename(), 'encoded-file.txt')
        self.assertEqual(attachment['Content-Disposition'], 'attachment; filename="encoded-file.txt"')

    def test_attachment_file_pdf(self):
        msg = Message()
        msg.attach_file('./tests/example.pdf')
        attachment = msg.attachments[0]
        self.assertEqual(attachment.get_content_type(), 'application/pdf')
        self.assertEqual(attachment.get_charset(), None)
        #self.assertEqual(attachment.get_payload(), u'')
        self.assertEqual(attachment.get_filename(), 'example.pdf')
        self.assertEqual(attachment['Content-Disposition'], 'attachment; filename="example.pdf"')

    def test_recipients(self):
        msg = Message(to='to@fluentmail.com',
                      cc=['cc1@fluentmail.com', 'cc2@fluentmail.com'],
                      bcc=['bcc1@fluentmail.com', 'bcc2@fluentmail.com'])
        recipients = msg.recipients()
        self.assertTrue('to@fluentmail.com' in recipients)
        self.assertTrue('cc1@fluentmail.com' in recipients)
        self.assertTrue('cc2@fluentmail.com' in recipients)
        self.assertTrue('bcc1@fluentmail.com' in recipients)
        self.assertTrue('bcc2@fluentmail.com' in recipients)

    def test_raw_message(self):
        msg = Message('FluentMail', 'Python SMTP client and Email for Humans™')
        raw = msg.raw_message()
        # TODO


class TestUtils(unittest.TestCase):

    def test_sanitize_address(self):
        email = sanitize_address('fluentmail@fluentmail.com')
        self.assertEqual(email, 'fluentmail@fluentmail.com')

    def test_sanitize_address_alias(self):
        email = sanitize_address('FluentMail <fluentmail@fluentmail.com>')
        self.assertEqual(email, 'FluentMail <fluentmail@fluentmail.com>')

    def test_sanitize_address_tuple(self):
        email = sanitize_address(('FluentMail', 'fluentmail@fluentmail.com'))
        self.assertEqual(email, 'FluentMail <fluentmail@fluentmail.com>')

    def test_sanitize_address_portuguese(self):
        email = sanitize_address((u'Acentuação', 'fluentmail@fluentmail.com'))
        if PY3:
            self.assertEqual(email, u'=?utf-8?b?QWNlbnR1YcOnw6Nv?= <fluentmail@fluentmail.com>')
        else:
            self.assertEqual(email, u'Acentuação <fluentmail@fluentmail.com>')

    def test_sanitize_address_russian(self):
        email = sanitize_address((u'говорить', 'fluentmail@fluentmail.com'))
        if PY3:
            self.assertEqual(email, u'=?utf-8?b?0LPQvtCy0L7RgNC40YLRjA==?= <fluentmail@fluentmail.com>')
        else:
            self.assertEqual(email, u'говорить <fluentmail@fluentmail.com>')

    def test_sanitize_address_list(self):
        email = sanitize_address_list([('FluentMail 1', 'fluentmail1@fluentmail.com'), ('FluentMail 2', 'fluentmail2@fluentmail.com')])
        self.assertEqual(email, ['FluentMail 1 <fluentmail1@fluentmail.com>', 'FluentMail 2 <fluentmail2@fluentmail.com>'])

    def test_join_address_list(self):
        email = join_address_list(['fluentmail@fluentmail.com'])
        self.assertEqual(email, 'fluentmail@fluentmail.com')

    def test_join_address_list_many(self):
        email = join_address_list([('FluentMail 1', 'fluentmail1@fluentmail.com'), ('FluentMail 2', 'fluentmail2@fluentmail.com')])
        self.assertEqual(email, 'FluentMail 1 <fluentmail1@fluentmail.com>, FluentMail 2 <fluentmail2@fluentmail.com>')

if __name__ == '__main__':
    unittest.main()
