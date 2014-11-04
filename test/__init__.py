#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unittest

from fluentmail import FluentMail, SSL, TLS

class TestFluentMail(unittest.TestCase):

    def test_plain_body(self):
        mail = FluentMail('smtp.you.com', 587, TLS)

        mail.credentials('you@you.com', 'pwd')\
            .from_address('you@you.com')\
            .to('other@you.com')\
            .subject('FluentMail')\
            .body(u'Hi, I\'m FluentMail.')

        msg = 'Content-Type: multipart/mixed; boundary="===============[0-9]+=="\n' +\
              'MIME-Version: 1.0\nFrom: you@you.com\nTo: other@you.com\nSubject: FluentMail\n\n' +\
              '--===============[0-9]+==\nContent-Type: text/plain; charset="utf-8"\n' +\
              'MIME-Version: 1.0\nContent-Transfer-Encoding: base64\n\nSGksIEknbSBGbHVlbnRNYWlsLg==\n\n' +\
              '--===============[0-9]+==--'

        self.assertTrue(re.match(msg, mail.raw_message()))

    def test_plain_kwargs(self):
        mail = FluentMail('smtp.you.com', 587, TLS, credentials=('you@you.com', 'pwd'))
        mail.body(u'Hi, I\'m FluentMail.')

        msg = 'Content-Type: multipart/mixed; boundary="===============[0-9]+=="\n' +\
              'MIME-Version: 1.0\nFrom: you@you.com\nTo: other@you.com\nSubject: FluentMail\n\n' +\
              '--===============[0-9]+==\nContent-Type: text/plain; charset="utf-8"\n' +\
              'MIME-Version: 1.0\nContent-Transfer-Encoding: base64\n\nSGksIEknbSBGbHVlbnRNYWlsLg==\n\n' +\
              '--===============[0-9]+==--'

        raw = mail.raw_message(from_address='you@you.com',
                               to='other@you.com',
                               subject='FluentMail')

        self.assertTrue(re.match(msg, raw))

if __name__ == '__main__':
    unittest.main()