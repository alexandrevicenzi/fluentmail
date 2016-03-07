## FluentMail [![Build Status](https://travis-ci.org/alexandrevicenzi/fluentmail.svg)](https://travis-ci.org/alexandrevicenzi/fluentmail) [![PyPI](https://img.shields.io/pypi/v/fluentmail.svg)](https://pypi.python.org/pypi/fluentmail)

Python SMTP client and Email for Humans&#8482;

## Simple

FluentMail tries to keep it simple as possible.

### SMTP client

With FluentMail

```python
from fluentmail import SMTP, TLS

client = SMTP('smtp.gmail.com', user='user', password='password', security=TLS)
client.send(message)
```

Pure Python

```python
import smtplib

client = smtplib.SMTP('smtp.gmail.com', 587)
client.starttls()
client.login('user', 'password')
client.sendmail('you@yourdomain.com', 'me@mydomain.com', '<RAW EMAIL MESSAGE>')
```

### Email message

With FluentMail

```python
message = EMailMessage('FluentMail', 'Python SMTP client and Email for Humans', from_address='you@yourdomain.com', to='me@mydomain.com')
message.attach_file('./photos/our-great-time-together.png')
```

Pure Python

```python
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid, formatdate

message = MIMEMultipart()
message['Subject'] = 'FluentMail'
message['From'] = 'you@yourdomain.com'
message['To'] = 'me@mydomain.com'
message['Date'] = formatdate()
message['Message-ID'] = make_msgid()
message.attach(MIMEText('Python SMTP client and Email for Humans', 'plain', 'utf-8'))

with open('./photos/our-great-time-together.png', 'rb') as f:
    message.attach(MIMEImage(f.read(), 'png'))
```

## Supported backends

- SMTP
- Mailgun (without attachment)
- Dummy (TODO)
- FileBased (TODO)
- MemoryBased (TODO)

## Install

`pip install fluentmail`

## Compatibility

Works with Python 2.6+, 3.3+ and PyPy.

## Documentation

TODO

## Future work

- Dummy backend
- FileBased backend
- MemoryBased backend
- Support template engines (Django, Jinja)
- Support Mailgun message attachment
- Support custom message headers
- Set default backend
- Thread-safety
- What more?
