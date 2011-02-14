# -*- coding: utf-8 -*-
from local_settings import *
import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__)) + '/'
TEMPLATE_DEBUG = DEBUG
TIME_ZONE = 'Europe/Bucharest'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = PROJECT_PATH + 'media/'
ADMIN_MEDIA_PREFIX = '/media/'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django_authopenid.context_processors.authopenid'
)

MIDDLEWARE_CLASSES = (
    'firepy.django.middleware.FirePHPMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django_authopenid.middleware.OpenIDMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

ROOT_URLCONF = 'snippify.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_PATH + 'templates'
)

INSTALLED_APPS = tuple([
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.syndication',
    'django.contrib.flatpages',
    'globaltags',
    'tagging',
    'django_authopenid',
    'djapian', #Should use haystack
    #'piston',
    'snippets',
] + DEV_APPS)

DJAPIAN_DATABASE_PATH = './djapian_spaces/'

# My settings
AUTH_PROFILE_MODULE = 'django_authopenid.UserProfile'
LOGIN_REDIRECT_URL = '/accounts/profile'
ACCOUNT_ACTIVATION_DAYS = 5
