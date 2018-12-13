"""
Django settings for webadmin project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "n)!1s@%4u$am)mly99g$&wum(8bbe=$7_#=uq=*6821do7x&=q"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
prueba = ''

# Application definition

INSTALLED_APPS = [
    # para poder ejecutar adminlte y hacer uso de sus templates
    "django_adminlte",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "graphene_django",
    "django_graphiql",
    "connections",
    "services",
    "main",
    "config",
]

GRAPHENE = {
    "SCHEMA": "webadmin.schema.schema",
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    #"django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

#=========================================================================================
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
from . import LDAP_settings

# Baseline configuration.

if len(LDAP_settings.AUTH_LDAP_SERVER_URI) > 0:
    AUTH_LDAP_SERVER_URI = LDAP_settings.AUTH_LDAP_SERVER_URI

if len(LDAP_settings.AUTH_LDAP_BIND_DN) > 0:
    AUTH_LDAP_BIND_DN = LDAP_settings.AUTH_LDAP_BIND_DN

if len(LDAP_settings.AUTH_LDAP_BIND_PASSWORD) > 0:
    AUTH_LDAP_BIND_PASSWORD = LDAP_settings.AUTH_LDAP_BIND_PASSWORD

AUTH_LDAP_PERMIT_EMPTY_PASSWORD = LDAP_settings.AUTH_LDAP_PERMIT_EMPTY_PASSWORD

if len(LDAP_settings.AUTH_LDAP_USER_DN_TEMPLATE) > 0:
    AUTH_LDAP_USER_DN_TEMPLATE = LDAP_settings.AUTH_LDAP_USER_DN_TEMPLATE

if len(LDAP_settings.AUTH_LDAP_USER_SEARCH) > 0:
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        LDAP_settings.AUTH_LDAP_USER_SEARCH,
        ldap.SCOPE_SUBTREE,
        '(uid=%(user)s)',
    )

if len(LDAP_settings.AUTH_LDAP_GROUP_SEARCH) > 0:
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
        LDAP_settings.AUTH_LDAP_GROUP_SEARCH,
        ldap.SCOPE_SUBTREE,
        '(objectClass=groupOfNames)',
    )
    AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr='cn')

    # Simple group restrictions
    if len(LDAP_settings.AUTH_LDAP_REQUIRE_GROUP) > 0:
        AUTH_LDAP_REQUIRE_GROUP = LDAP_settings.AUTH_LDAP_REQUIRE_GROUP

    if len(LDAP_settings.AUTH_LDAP_DENY_GROUP) > 0:
        AUTH_LDAP_REQUIRE_GROUP = LDAP_settings.AUTH_LDAP_DENY_GROUP

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = False

# Cache distinguised names and group memberships for an hour to minimize
# LDAP traffic.
AUTH_LDAP_CACHE_TIMEOUT = 3600

#========================================================================================



AUTHENTICATION_BACKENDS = [
    'webadmin.backends.LDAPBackend',
    'webadmin.backends.CustomBackend',
    'webadmin.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

GRAPHQL_JWT = {
    'JWT_ALLOW_ARGUMENT': False,
}

ROOT_URLCONF = "webadmin.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates/"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "webadmin.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "es-co"

TIME_ZONE = "America/Bogota"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"), os.path.join(BASE_DIR, "media"))
