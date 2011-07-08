from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^admin/', include('b3portal.rconadmin.urls')),
    url(r'^client/', include('b3portal.client.urls')),
    url(r'^server/', include('b3portal.server.urls')),
    url(r'^maps/$', views.maps, name='map_list'),
    url(r'^banned/map/$', views.banned_player_map, name='banned_world_map'),
    url(r'^banned/search/$', views.banlist, name='search_ban_list'),
    url(r'^banned/kicks/$', views.kicklist, name='admin_kicks'),
    url(r'^banned/last/$', views.penalty_list, name='penalty_list'),
    url(r'^banned/notices/$', views.notice_list, name='notice_list'),
    url(r'^banned/$', views.banlist, name='ban_list'),
)