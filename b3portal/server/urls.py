from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^add/$', views.edit_server, name='add_server'),
    url(r'^edit/(?P<slug>[-\w]+)/$', views.edit_server, name='edit_server'),
#    url(r'^$', views.clientlist, name='client_list'),
)