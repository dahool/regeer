from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
import views

urlpatterns = patterns('',
    url(r'^$', views.chatlist, name='chat_list'),
)