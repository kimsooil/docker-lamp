"""
WSGI config for dcc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import environ
from django.core.wsgi import get_wsgi_application
ENV = environ.Env()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', ENV('DJANGO_SETTINGS_MODULE'))

application = get_wsgi_application()
