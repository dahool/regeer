from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='follow_home'),
    url(r'^add/(?P<id>[0-9]+)/$', views.add, name='follow_add'),
    url(r'^del/(?P<id>[0-9]+)/$', views.remove, name='follow_remove'),
)