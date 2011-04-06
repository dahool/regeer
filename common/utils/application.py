from django.conf import settings

def is_installed(name):
    return name in settings.INSTALLED_APPS
    
def is_plugin_installed(name):
    return is_installed('plugins.%s' % name)