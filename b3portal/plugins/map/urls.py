from django.conf.urls.defaults import *
from b3portal.plugins.map import views

urlpatterns = patterns('',
    url(r'^$', views.maps, name='home'),
)