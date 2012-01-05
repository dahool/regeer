from django.conf import settings

def is_installed(name):
    return name in settings.INSTALLED_APPS