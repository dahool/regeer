from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^map/$', views.banned_player_map, name='banned_world_map'),
    url(r'^search/$', views.banlist, name='search_ban_list'),
    url(r'^kicks/$', views.kicklist, name='admin_kicks'),
    url(r'^last/$', views.penalty_list, name='penalty_list'),
    url(r'^notices/$', views.notice_list, name='notice_list'),
    url(r'^$', views.banlist, name='ban_list'),
)