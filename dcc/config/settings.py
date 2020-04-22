"""
Imports everything from base.py

Use this for project specific settings.

NOTE: This file should only be updated in a project specific project, not from DCC.
"""

import environ
from .base import *

ENV = environ.Env()

MODEL_API_BASE_URL = ENV('MODEL_API_BASE_URL', default='http://localhost:5000/')
MODEL_API_SUBPATH = ENV('MODEL_API_SUBPATH', default='/model/')
MODEL_API_STATE = ENV('MODEL_API_STATE', default='Nebraska')

API_DEFAULT_COUNTIES = ENV.list('DJANGO_API_DEFAULT_COUNTIES', default=['Lincoln'])
API_DEFAULT_MAP_X_COORD = ENV('DJANGO_API_DEFAULT_MAP_X_COORD', default='41.5')
API_DEFAULT_MAP_Y_COORD = ENV('DJANGO_API_DEFAULT_MAP_Y_COORD', default='-100.0')
API_DEFAULT_MAP_ZOOM_LEVEL = ENV.int('DJANGO_API_DEFAULT_MAP_ZOOM_LEVEL', default=3)


