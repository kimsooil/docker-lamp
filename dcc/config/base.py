"""
Django settings for dcc project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
# from os import environ as ENV
import environ
ENV = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# Use this one if dcc/development.py
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Use this if dcc/settings/development.py
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'qezyue5wcapkr@5d(_-n4pxo!(gjkr*kcpve)r@4m*6o$wx$jm'
# Use a separate file for the secret key
with open(os.path.join(BASE_DIR, 'secretkey.txt')) as f:
    SECRET_KEY = f.read().strip()

# SECRET_KEY = ENV['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if ENV('ENVIRONMENT') == 'production' else True

ALLOWED_HOSTS = ENV.list('DJANGO_ALLOWED_HOSTS', default=['localhost','127.0.0.1'])

# Wagtail.
WAGTAIL_SITE_NAME = 'Django Cookie Cutter!'

# APPS
# ------------------------------------------------------------------------------

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    # Django Rest Framework.
    'rest_framework',
    # 'rest_framework_swagger',
    'rest_framework.authtoken',

    # # Allows for generating secret key.
    # 'django_generate_secret_key',

    # Wagtail.
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',

    # For the users app.
    'crispy_forms',

    # CORS.
    'corsheaders',

    # Django OAuth Toolkit
    'oauth2_provider',
]

OAUTH2_PROVIDER = {
# other OAUTH2 settings
'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore'
}

# If not production, add rest framework.
if not ENV('ENVIRONMENT') == 'production':
    THIRD_PARTY_APPS.append('rest_framework_swagger')

LOCAL_APPS = [
    'users.apps.UsersAppConfig',
    # Your stuff: custom apps go here
]

# # https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'users.User'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
# LOGIN_REDIRECT_URL = 'users:redirect'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
# LOGIN_URL = 'account_login'

MIDDLEWARE = [
    # DEFAULT
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # CORES - This needs to be here so it can inject the headers before responses (CommonMiddleware).
    'corsheaders.middleware.CorsMiddleware',

    # MORE DEFAULT
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Wagtail.
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

# False by default, but, can be modified to True for mobile applications.
CORS_ORIGIN_ALLOW_ALL = True

# # Whitelist can be used for development purposes.
# CORS_ORIGIN_WHITELIST = (
#     'google.com',
#     'hostname.example.com',
#     'localhost:8000',
#     '127.0.0.1:9000'
# )

ROOT_URLCONF = 'dcc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'dcc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Local settings file which is not added to the repository. Use this for saving passwords.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ENV('POSTGRES_DB'),
        'USER': ENV('POSTGRES_USER'),
        'PASSWORD': ENV('POSTGRES_PASSWORD'),
        'HOST': ENV('POSTGRES_HOST', default='localhost'),
        'PORT': ENV('POSTGRES_PORT', default='5432'),
    }
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Django rest framework authentication scheme.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}

# Email settings.
EMAIL_BACKEND = ENV('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = ENV('DJANGO_EMAIL_HOST', default='localhost')
EMAIL_PORT = ENV('DJANGO_EMAIL_PORT', default='25')

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Get the timezone from the system.
TIME_ZONE = os.getenv('TIME_ZONE', "America/Indianapolis")

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
    '/var/www/static/',
]

MEDIA_ROOT = '/media/' if ENV('ENVIRONMENT') == 'production' else os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'