# -*- coding: utf-8 -*-

__all__ = ['sanitize_address', 'sanitize_address_list', 'join_address_list', 'PY3', 'text_type', 'string_type']

import sys

from email.utils import parseaddr, formataddr

PY3 = sys.version_info[0] == 3

if PY3:
    text_type = str
    string_type = (str,)
else:
    text_type = unicode
    string_type = (str, unicode)


def sanitize_address(address):
    if not isinstance(address, tuple):
        address = parseaddr(address)
    name, email = address
    return formataddr((name, email))


def sanitize_address_list(addresses):
    return [sanitize_address(address) for address in addresses]


def join_address_list(addresses):
    return ', '.join(sanitize_address_list(addresses))
