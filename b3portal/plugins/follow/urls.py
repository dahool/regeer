from django.conf.urls.defaults import *
from b3portal.plugins.follow import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^add/(?P<id>[0-9]+)/$', views.add, name='add'),
    url(r'^del/(?P<id>[0-9]+)/$', views.remove, name='remove'),
)