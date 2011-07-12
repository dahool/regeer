from django.conf.urls.defaults import *
from b3portal.plugins import PLUGINS
from b3portal.plugins import is_plugin_installed

import views

urlpatterns = patterns('',
    url(r'^$', views.home),
    #url(r'^rcon/', include('b3portal.rconadmin.urls')),
    url(r'^client/', include('b3portal.client.urls')),
    url(r'^banned/', include('b3portal.penalties.urls')),
    url(r'^maps/$', views.maps, name='map_list'),
)

for plugin in PLUGINS:
    if is_plugin_installed(plugin[0]):
        s = "b3portal.plugins.%s.urls" % plugin[0]
        urlpatterns += patterns('',
            url(r'^%s/' % plugin[0], include(s, namespace="plugin"))
        )