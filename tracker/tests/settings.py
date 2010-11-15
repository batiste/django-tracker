# Django settings for testproj project.

import os
import sys
# import source code dir
sys.path.insert(0, os.path.join(os.getcwd(), os.pardir))

SITE_ID = 69932

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT_URLCONF = "urls"

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

COVERAGE_EXCLUDE_MODULES = ("opalhtml.tests.*", )

here = os.path.abspath(os.path.dirname(__file__))

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'testdb.sqlite'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

CACHE_BACKEND = 'locmem://'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'tracker',
)
