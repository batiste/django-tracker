#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
from setuptools import setup, find_packages

import tracker

def local_open(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))

import os
data_dirs = []
for directory in os.walk('pages/templates'):
    data_dirs.append(directory[0][6:] + '/*.*')

for directory in os.walk('pages/media'):
    data_dirs.append(directory[0][6:] + '/*.*')

setup(
    name='django-tracker',
    version=tracker.__version__,
    description=tracker.__doc__,
    author=tracker.__author__,
    author_email=tracker.__contact__,
    url=tracker.__homepage__,
    platforms=["any"],
    packages=find_packages(exclude=['testproj', 'testproj.*']),
    package_data={'pages': data_dirs},
    zip_safe=False,
    install_requires=[
        'Django'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description=local_open('README.rst').read(),
)
