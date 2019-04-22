# settings.py

## Purpose

This readme discusses how the *dcc/config/base.py* and *dcc/config/settings.py* are setup.

## base.py

base.py file includes all the CC settings for the project. 

## settings.py

settings.py imports ALL the settings from base.py. The file is then left black to allow for project specific code. In addition, this allows for Django to remain as close to the default structure as possible. In other words, projects simply do the following to impor the settings.

```py
from django.contrib.config import settings
```