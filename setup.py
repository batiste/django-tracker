#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
from setuptools import setup, find_packages, Command

import tracker

def local_open(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))

import os
data_dirs = []
for directory in os.walk('pages/templates'):
    data_dirs.append(directory[0][6:] + '/*.*')

for directory in os.walk('pages/media'):
    data_dirs.append(directory[0][6:] + '/*.*')

class RunTests(Command):
    description = "Run the django test suite from the tests dir."

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        this_dir = os.getcwd()
        testproj_dir = os.path.join(this_dir, "tracker/tests")
        os.chdir(testproj_dir)
        sys.path.insert(0, testproj_dir)
        from django.core.management import execute_manager
        os.environ["DJANGO_SETTINGS_MODULE"] = os.environ.get(
                        "DJANGO_SETTINGS_MODULE", "settings")
        settings_file = os.environ["DJANGO_SETTINGS_MODULE"]
        settings_mod = __import__(settings_file, {}, {}, [""])
        execute_manager(settings_mod, argv=[
            __file__, "test"])
        os.chdir(this_dir)

setup(
    name='django-tracker',
    version=tracker.__version__,
    description=tracker.__doc__,
    author=tracker.__author__,
    author_email=tracker.__contact__,
    url=tracker.__homepage__,
    cmdclass={"test": RunTests},
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
