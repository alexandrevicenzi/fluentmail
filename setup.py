#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='fluentmail',
    version='1.0.0',
    author='Alexandre Vicenzi',
    author_email='pypi@alxd.me',
    maintainer='Alexandre Vicenzi',
    maintainer_email='pypi@alxd.me',
    packages=find_packages(exclude=("tests",)),
    url='https://github.com/alexandrevicenzi/fluentmail',
    bugtrack_url='https://github.com/alexandrevicenzi/fluentmail/issues',
    license='MIT',
    description='Tiny library to send email',
    long_description=long_description,
    keywords='python, email, mail, smtp, mailgun',
    platforms='',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Communications :: Email',
        'Topic :: Utilities',
    ],
)
