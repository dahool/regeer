from django.conf.urls.defaults import *
import views
from common.view.decorators import render

urlpatterns = patterns('',
    url(r'^$', views.home, name='game_admin'),
    url(r'^execute/$', views.execute, name='admin_command'),
    url(r'^ref/clients/$', views.refresh_clients, name='admin_refresh_clients'),
    url(r'^ref/status/$', views.refresh_status, name='admin_refresh_status'),
    url(r'^ban/list/$', views.banlist, name='admin_ban_list'),
    url(r'^group/list/$', views.group_list, name='group_list_json'),
)