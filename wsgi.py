#!/usr/bin/python
import os, sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "regeer.settings")

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
