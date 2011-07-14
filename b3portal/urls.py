from django.conf.urls.defaults import *
from b3portal.plugins import PLUGINS
from b3portal.plugins import is_plugin_installed
from django.conf import settings

import views

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^client/', include('b3portal.client.urls')),
    url(r'^banned/', include('b3portal.penalties.urls')),
)

if settings.B3_INSTALLED:
    urlpatterns += patterns('',
        url(r'^rcon/', include('b3portal.rconadmin.urls')),
    )    

for plugin in PLUGINS:
    if is_plugin_installed(plugin[0]):
        app = plugin[0]
        urlpatterns += patterns('',
            url(r'^%s/' % app, include("b3portal.plugins.%s.urls" % app, namespace=app))
        )