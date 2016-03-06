#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('./../')

import unittest

from base64 import b64encode
from fluentmail import EMailMessage, sanitize_address, sanitize_address_list, join_address_list


class TestEMailMessage(unittest.TestCase):

    def test_body_plain(self):
        msg = EMailMessage('FluentMail', 'The tiny library to send emails',
                           from_address='sender@fluentmail.com', to='receiver@fluentmail.com')
        mime = msg.message()
        body = mime.get_payload()[0]
        self.assertEquals(body.get_content_type(), 'text/plain')
        self.assertEquals(body.get_charset(), 'utf-8')
        self.assertEquals(body.get_payload(), '%s\n' % b64encode('The tiny library to send emails'))

    def test_body_plain_russian(self):
        msg = EMailMessage('FluentMail', u'К сожалению, мы должны сообщить',
                           from_address='sender@fluentmail.com', to='receiver@fluentmail.com')
        mime = msg.message()
        body = mime.get_payload()[0]
        self.assertEquals(body.get_content_type(), 'text/plain')
        self.assertEquals(body.get_charset(), 'utf-8')
        self.assertEquals(body.get_payload(), '%s\n' % b64encode(u'К сожалению, мы должны сообщить'.encode('utf-8')))

    def test_body_plain_chinese(self):
        msg = EMailMessage('FluentMail', u'我的测试文档',
                           from_address='sender@fluentmail.com', to='receiver@fluentmail.com')
        mime = msg.message()
        body = mime.get_payload()[0]
        self.assertEquals(body.get_content_type(), 'text/plain')
        self.assertEquals(body.get_charset(), 'utf-8')
        self.assertEquals(body.get_payload(), '%s\n' % b64encode(u'我的测试文档'.encode('utf-8')))

    def test_body_html(self):
        msg = EMailMessage('FluentMail', '<b>The tiny library to send emails<b>', html=True,
                           from_address='sender@fluentmail.com', to='receiver@fluentmail.com')
        mime = msg.message()
        body = mime.get_payload()[0]
        self.assertEquals(body.get_content_type(), 'text/html')
        self.assertEquals(body.get_charset(), 'utf-8')
        self.assertEquals(body.get_payload(), '%s\n' % b64encode('<b>The tiny library to send emails<b>'))

    def test_body_encoding(self):
        msg = EMailMessage('FluentMail', u'Acentuação é um negócio do Português', encoding='iso-8859-1',
                           from_address='sender@fluentmail.com', to='receiver@fluentmail.com')
        mime = msg.message()
        body = mime.get_payload()[0]
        self.assertEquals(body.get_content_type(), 'text/plain')
        self.assertEquals(body.get_charset(), 'iso-8859-1')
        self.assertEquals(body.get_payload(), 'Acentua=E7=E3o =E9 um neg=F3cio do Portugu=EAs')

    def test_attachment(self):
        msg = EMailMessage()
        msg.attach('myfile.txt', 'my content', 'text/plain')
        attachment = msg.attachments[0]
        self.assertEquals(attachment.get_content_type(), 'text/plain')
        self.assertEquals(attachment.get_charset(), 'utf-8')
        self.assertEquals(attachment.get_payload(), 'bXkgY29udGVudA==\n')
        self.assertEquals(attachment.get_filename(), 'myfile.txt')
        self.assertEquals(attachment['Content-Disposition'], 'attachment; filename="myfile.txt"')

    def test_attachment_encoding(self):
        msg = EMailMessage()
        msg.attach('myfile.txt', u'Acentuação é um negócio do Português', 'text/plain', 'iso-8859-1')
        attachment = msg.attachments[0]
        self.assertEquals(attachment.get_content_type(), 'text/plain')
        self.assertEquals(attachment.get_charset(), 'iso-8859-1')
        self.assertEquals(attachment.get_payload(), u'Acentua=E7=E3o =E9 um neg=F3cio do Portugu=EAs')
        self.assertEquals(attachment.get_filename(), 'myfile.txt')
        self.assertEquals(attachment['Content-Disposition'], 'attachment; filename="myfile.txt"')

    def test_attachment_file_encoded(self):
        msg = EMailMessage()
        msg.attach_file('./tests/encoded-file.txt', 'text/plain', 'iso-8859-1')
        attachment = msg.attachments[0]
        self.assertEquals(attachment.get_content_type(), 'text/plain')
        self.assertEquals(attachment.get_charset(), 'utf-8')
        self.assertEquals(attachment.get_payload(), 'QWNlbnR1YcOnw6NvIMOpIHVtIG5lZ8OzY2lvIGRvIFBvcnR1Z3XDqnM=\n')
        self.assertEquals(attachment.get_filename(), 'encoded-file.txt')
        self.assertEquals(attachment['Content-Disposition'], 'attachment; filename="encoded-file.txt"')

    def test_attachment_file_pdf(self):
        msg = EMailMessage()
        msg.attach_file('./tests/example.pdf')
        attachment = msg.attachments[0]
        self.assertEquals(attachment.get_content_type(), 'application/pdf')
        self.assertEquals(attachment.get_charset(), 'utf-8')
        #self.assertEquals(attachment.get_payload(), u'')
        self.assertEquals(attachment.get_filename(), 'example.pdf')
        self.assertEquals(attachment['Content-Disposition'], 'attachment; filename="example.pdf"')


class TestUtils(unittest.TestCase):

    def test_sanitize_address(self):
        email = sanitize_address('fluentmail@fluentmail.com')
        self.assertEquals(email, 'fluentmail@fluentmail.com')

    def test_sanitize_address_alias(self):
        email = sanitize_address('FluentMail <fluentmail@fluentmail.com>')
        self.assertEquals(email, 'FluentMail <fluentmail@fluentmail.com>')

    def test_sanitize_address_tuple(self):
        email = sanitize_address(('FluentMail', 'fluentmail@fluentmail.com'))
        self.assertEquals(email, 'FluentMail <fluentmail@fluentmail.com>')

    def test_sanitize_address_portuguese(self):
        email = sanitize_address((u'Acentuação', 'fluentmail@fluentmail.com'))
        self.assertEquals(email, u'Acentuação <fluentmail@fluentmail.com>')

    def test_sanitize_address_russian(self):
        email = sanitize_address((u'говорить', 'fluentmail@fluentmail.com'))
        self.assertEquals(email, u'говорить <fluentmail@fluentmail.com>')

    def test_sanitize_address_list(self):
        email = sanitize_address_list([('FluentMail 1', 'fluentmail1@fluentmail.com'), ('FluentMail 2', 'fluentmail2@fluentmail.com')])
        self.assertEquals(email, ['FluentMail 1 <fluentmail1@fluentmail.com>', 'FluentMail 2 <fluentmail2@fluentmail.com>'])

    def test_join_address_list(self):
        email = join_address_list(['fluentmail@fluentmail.com'])
        self.assertEquals(email, 'fluentmail@fluentmail.com')

    def test_join_address_list_many(self):
        email = join_address_list([('FluentMail 1', 'fluentmail1@fluentmail.com'), ('FluentMail 2', 'fluentmail2@fluentmail.com')])
        self.assertEquals(email, 'FluentMail 1 <fluentmail1@fluentmail.com>, FluentMail 2 <fluentmail2@fluentmail.com>')

if __name__ == '__main__':
    unittest.main()
