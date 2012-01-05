#!/usr/bin/python
import os, sys
sys.path.insert(0, '/your/application/path')
sys.path.insert(1, '/your/application/path/regeer')

os.environ['DJANGO_SETTINGS_MODULE'] = 'regeer.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()