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


