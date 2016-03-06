# -*- coding: utf-8 -*-

__all__ = ['sanitize_address', 'sanitize_address_list', 'join_address_list']

from email.utils import parseaddr, formataddr


def sanitize_address(address):
    if not isinstance(address, tuple):
        address = parseaddr(address)
    name, email = address
    return formataddr((name, email))


def sanitize_address_list(addresses):
    return [sanitize_address(address) for address in addresses]


def join_address_list(addresses):
    return ', '.join(sanitize_address_list(addresses))
