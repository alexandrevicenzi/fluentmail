## FluentMail [![Build Status](https://travis-ci.org/alexandrevicenzi/fluentmail.svg)](https://travis-ci.org/alexandrevicenzi/fluentmail) [![PyPI](https://img.shields.io/pypi/v/fluentmail.svg)](https://pypi.python.org/pypi/fluentmail)

Tiny library to send email

## Install

`pip install fluentmail`

or

`python setup.py install`

## Compatibility

Works with Python 2.6+, 3.3+ and PyPy.

## Usage

### Basic

```python
with SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=SSL) as backend:
    msg = EMailMessage('FluentMail SSL', 'The tiny library to send emails',
                       from_address=FROM, to=TO)
    msg.send(backend)
```

or

```python
backend = SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=TLS)
msg = EMailMessage('FluentMail Without With Block', 'The tiny library to send emails',
                   from_address=FROM, to=TO)
backend.send(msg)
```

### Multiple messages

```python
with SMTP('smtp.gmail.com', user=GMAIL_USER, password=GMAIL_PWD, security=TLS) as backend:
    msg1 = EMailMessage('FluentMail', 'The tiny library to send emails',
                        from_address=FROM, to=TO)
    msg2 = EMailMessage('FluentMail', 'The tiny library to send emails',
                        from_address=FROM, to=TO)
    backend.send_multiple([msg1, msg2])
```

Take a look in `examples` to see more examples.

## Common smtp servers

| Name  | Server | Authentication | Port |
|:----|:--------:|:--------------:|:----:|
|Gmail|smtp.gmail.com|SSL|465|
|Gmail|smtp.gmail.com|StartTLS|587|
|Hotmail|smtp.live.com|SSL|465|
|Mail.com|smtp.mail.com|SSL|465|
|Outlook.com|smtp.live.com|StartTLS|587|
|Office365.com|smtp.office365.com|StartTLS|587|
|Yahoo Mail|smtp.mail.yahoo.com|SSL|465|

For GMail you may want to read [this](https://www.google.com/settings/security/lesssecureapps) security info.
