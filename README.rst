fluentmail |Build Status| |Version|
===================================

Tiny library to send email fluently

Install
-------

``pip install fluentmail``

Usage
-----

Basic
~~~~~

.. code:: python

    from fluentmail import FluentMail

    mail = FluentMail('smtp.gmail.com', 587, TLS)

    mail.credentials('you@gmail.com', 'pwd')\
        .from_address('you@gmail.com')\
        .to('other@gmail.com')\
        .subject('FluentMail')\
        .body(u'Hi, I\'m FluentMail.')\
        .send()

HTML Body
~~~~~~~~~

.. code:: python

    from fluentmail import FluentMail

    mail = FluentMail('smtp.gmail.com', 587, TLS)

    mail.credentials('you@gmail.com', 'pwd')\
        .from_address('you@gmail.com')\
        .to('other@gmail.com')\
        .subject('FluentMail')\
        .body(u'<h2>Hi, I\'m FluentMail.<h2>')\
        .as_html()\
        .send()

With Attachment
~~~~~~~~~~~~~~~

.. code:: python

    from fluentmail import FluentMail

    mail = FluentMail('smtp.gmail.com', 587, TLS)

    mail.credentials('you@gmail.com', 'pwd')\
        .from_address('you@gmail.com')\
        .to('other@gmail.com')\
        .subject('FluentMail')\
        .body(u'<h2>Hi, I\'m FluentMail.<h2>', 'utf-8')\ # Body charset is optional.
        .as_html()\
        .attach('photo.png')\
        .attach('description.txt', 'utf-8')\ # Charset is optional, and only for Text files.
        .send()

Authentication type
~~~~~~~~~~~~~~~~~~~

NON\_ENCRYPTED
^^^^^^^^^^^^^^

::

    mail = FluentMail('smtp.yoursite.com', 25, NON_ENCRYPTED)

SSL
^^^

::

    mail = FluentMail('smtp.yoursite.com', 465, SSL)

TLS
^^^

::

    mail = FluentMail('smtp.yoursite.com', 587, TLS)

By default SSL uses port 465, TLS uses 587 and AUTH 25.

For GMail you may want to read `this`_ security info.

Common smtp servers
-------------------

+-----------------+-----------------------+------------------+--------+
| Name            | Server                | Authentication   | Port   |
+=================+=======================+==================+========+
| Gmail           | smtp.gmail.com        | SSL              | 465    |
+-----------------+-----------------------+------------------+--------+
| Gmail           | smtp.gmail.com        | StartTLS         | 587    |
+-----------------+-----------------------+------------------+--------+
| Hotmail         | smtp.live.com         | SSL              | 465    |
+-----------------+-----------------------+------------------+--------+
| Mail.com        | smtp.mail.com         | SSL              | 465    |
+-----------------+-----------------------+------------------+--------+
| Outlook.com     | smtp.live.com         | StartTLS         | 587    |
+-----------------+-----------------------+------------------+--------+
| Office365.com   | smtp.office365.com    | StartTLS         | 587    |
+-----------------+-----------------------+------------------+--------+
| Yahoo Mail      | smtp.mail.yahoo.com   | SSL              | 465    |
+-----------------+-----------------------+------------------+--------+

.. _this: https://www.google.com/settings/security/lesssecureapps

.. |Build Status| image:: https://travis-ci.org/alexandrevicenzi/fluentmail.svg?branch=master
   :target: https://travis-ci.org/alexandrevicenzi/fluentmail
.. |Version| image:: https://pypip.in/version/fluentmail/badge.png
   :target: https://pypi.python.org/pypi/fluentmail