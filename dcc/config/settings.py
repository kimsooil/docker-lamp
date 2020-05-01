"""
Imports everything from base.py

Use this for project specific settings.

NOTE: This file should only be updated in a project specific project, not from DCC.
"""

import environ
from .base import *

ENV = environ.Env()

# Setup support for proxy headers
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

MODEL_API_BASE_URL = ENV('MODEL_API_BASE_URL', default='http://localhost:5000/')
MODEL_API_SUBPATH = ENV('MODEL_API_SUBPATH', default='/model/')
MODEL_API_STATE = ENV('MODEL_API_STATE', default='Nebraska')
MODEL_API_STATE_ABBREVIATION = ENV('MODEL_API_STATE_ABBREVIATION', default='NE')
MODEL_API_COUNTRY = ENV('MODEL_API_COUNTRY', default='US')

API_DEFAULT_COUNTIES = ENV.list('DJANGO_API_DEFAULT_COUNTIES', default=['Lincoln'])
API_DEFAULT_MAP_X_COORD = ENV('DJANGO_API_DEFAULT_MAP_X_COORD', default='41.5')
API_DEFAULT_MAP_Y_COORD = ENV('DJANGO_API_DEFAULT_MAP_Y_COORD', default='-100.0')
API_DEFAULT_MAP_ZOOM_LEVEL = ENV.int('DJANGO_API_DEFAULT_MAP_ZOOM_LEVEL', default=3)
API_DEFAULT_SHELTER_DATE = ENV.str('DJANGO_API_DEFAULT_SHELTER_DATE', default='2020-04-03')
API_DEFAULT_SHELTER_END_DATE = ENV.str('DJANGO_API_DEFAULT_SHELTER_END_DATE', default='2020-08-01')
API_DEFAULT_SIM_LENGTH = ENV.int('DJANGO_API_DEFAULT_SIM_LENGTH', default=56)
API_DEFAULT_NDRAWS = ENV.int('DJANGO_API_DEFAULT_NDRAWS', default=50000)

