#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('LICENSE') as f:
    license = f.read()

with open('README.rst') as f:
    description = f.read()

setup(
    name='fluentmail',
    version='0.1.1',
    author='Alexandre Vicenzi',
    author_email='vicenzi.alexandre@gmail.com',
    maintainer='Alexandre Vicenzi',
    maintainer_email='vicenzi.alexandre@gmail.com',
    packages=['fluentmail'],
    url='https://github.com/alexandrevicenzi/fluentmail',
    bugtrack_url='https://github.com/alexandrevicenzi/fluentmail/issues',
    license=license,
    description='Tiny library to send email fluently',
    long_description=description,
    keywords='python, email, mail, fluent, smtp',
    platforms='',
    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS',
          'Operating System :: Microsoft',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Topic :: Communications :: Email',
          'Topic :: Utilities',
          ],
)
