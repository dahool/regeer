from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^rcon/', include('b3portal.rconadmin.urls')),
    url(r'^client/', include('b3portal.client.urls')),
    url(r'^server/', include('b3portal.server.urls')),
    url(r'^banned/', include('b3portal.penalties.urls')),
    url(r'^maps/$', views.maps, name='map_list'),
)