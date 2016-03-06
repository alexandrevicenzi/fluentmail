#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest

from fluentmail import EMailMessage, sanitize_address, sanitize_address_list, join_address_list

PY3 = sys.version_info.major == 3


class TestEMailMessage(unittest.TestCase):

    def test_body_plain(self):
        msg = EMailMessage('FluentMail', 'The tiny library to send emails',
                           from_address='sender@fluentmail.com', to='receiver@fluentmail.com')
        mime = msg.message()
        body = mime.get_payload()[0]
        self.assertEqual(body.get_content_type(), 'text/plain')
        self.assertEqual(body.get_charset(), 'utf-8')
        self.assertEqual(body.get_payload(), 'VGhlIHRpbnkgbGlicmFyeSB0byBzZW5kIGVtYWlscw==\n')

    def test_body_plain_russian(self):
        msg = EMailMessage('FluentMail', u'К сожалению, мы должны сообщить',
                           from_address='sender@fluentmail.com', to='receiver@fluentmail.com')
        mime = msg.message()
        body = mime.get_payload()[0]
        self.assertEqual(body.get_content_type(), 'text/plain')
        self.assertEqual(body.get_charset(), 'utf-8')
        self.assertEqual(body.get_payload(), '0Jog0YHQvtC20LDQu9C10L3QuNGOLCDQvNGLINC00L7Qu9C20L3RiyDRgdC+0L7QsdGJ0LjRgtGM\n')

    def test_body_plain_chinese(self):
        msg = EMailMessage('FluentMail', u'我的测试文档',
                           from_address='sender@fluentmail.com', to='receiver@fluentmail.com')
        mime = msg.message()
        body = mime.get_payload()[0]
        self.assertEqual(body.get_content_type(), 'text/plain')
        self.assertEqual(body.get_charset(), 'utf-8')
        self.assertEqual(body.get_payload(), '5oiR55qE5rWL6K+V5paH5qGj\n')

    def test_body_html(self):
        msg = EMailMessage('FluentMail', '<b>The tiny library to send emails<b>', html=True,
                           from_address='sender@fluentmail.com', to='receiver@fluentmail.com')
        mime = msg.message()
        body = mime.get_payload()[0]
        self.assertEqual(body.get_content_type(), 'text/html')
        self.assertEqual(body.get_charset(), 'utf-8')
        self.assertEqual(body.get_payload(), 'PGI+VGhlIHRpbnkgbGlicmFyeSB0byBzZW5kIGVtYWlsczxiPg==\n')

    def test_body_encoding(self):
        msg = EMailMessage('FluentMail', u'Acentuação é um negócio do Português', encoding='iso-8859-1',
                           from_address='sender@fluentmail.com', to='receiver@fluentmail.com')
        mime = msg.message()
        body = mime.get_payload()[0]
        self.assertEqual(body.get_content_type(), 'text/plain')
        self.assertEqual(body.get_charset(), 'iso-8859-1')
        self.assertEqual(body.get_payload(), 'Acentua=E7=E3o =E9 um neg=F3cio do Portugu=EAs')

    def test_attachment(self):
        msg = EMailMessage()
        msg.attach('myfile.txt', 'my content', 'text/plain')
        attachment = msg.attachments[0]
        self.assertEqual(attachment.get_content_type(), 'text/plain')
        self.assertEqual(attachment.get_charset(), 'utf-8')
        self.assertEqual(attachment.get_payload(), 'bXkgY29udGVudA==\n')
        self.assertEqual(attachment.get_filename(), 'myfile.txt')
        self.assertEqual(attachment['Content-Disposition'], 'attachment; filename="myfile.txt"')

    def test_attachment_encoding(self):
        msg = EMailMessage()
        msg.attach('myfile.txt', u'Acentuação é um negócio do Português', 'text/plain', 'iso-8859-1')
        attachment = msg.attachments[0]
        self.assertEqual(attachment.get_content_type(), 'text/plain')
        self.assertEqual(attachment.get_charset(), 'iso-8859-1')
        self.assertEqual(attachment.get_payload(), u'Acentua=E7=E3o =E9 um neg=F3cio do Portugu=EAs')
        self.assertEqual(attachment.get_filename(), 'myfile.txt')
        self.assertEqual(attachment['Content-Disposition'], 'attachment; filename="myfile.txt"')

    def test_attachment_file_encoded(self):
        msg = EMailMessage()
        msg.attach_file('./tests/encoded-file.txt', 'text/plain', 'iso-8859-1')
        attachment = msg.attachments[0]
        self.assertEqual(attachment.get_content_type(), 'text/plain')
        self.assertEqual(attachment.get_charset(), 'utf-8')
        self.assertEqual(attachment.get_payload(), 'QWNlbnR1YcOnw6NvIMOpIHVtIG5lZ8OzY2lvIGRvIFBvcnR1Z3XDqnM=\n')
        self.assertEqual(attachment.get_filename(), 'encoded-file.txt')
        self.assertEqual(attachment['Content-Disposition'], 'attachment; filename="encoded-file.txt"')

    def test_attachment_file_pdf(self):
        msg = EMailMessage()
        msg.attach_file('./tests/example.pdf')
        attachment = msg.attachments[0]
        self.assertEqual(attachment.get_content_type(), 'application/pdf')
        self.assertEqual(attachment.get_charset(), 'utf-8')
        #self.assertEqual(attachment.get_payload(), u'')
        self.assertEqual(attachment.get_filename(), 'example.pdf')
        self.assertEqual(attachment['Content-Disposition'], 'attachment; filename="example.pdf"')


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
