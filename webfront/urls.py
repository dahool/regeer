from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='web_home'),
    url(r'^admin/', include('webfront.rconadmin.urls')),
    url(r'^client/', include('webfront.client.urls')),
    url(r'^server/', include('webfront.server.urls')),
    url(r'^login/$', auth_views.login, kwargs={'template_name':'auth/login.html'}, name='user_signin'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/' }, name='auth_logout'),
    url(r'^maps/$', views.maps, name='map_list'),
    url(r'^banned/map/$', views.banned_player_map, name='banned_world_map'),
    url(r'^banned/search/$', views.banlist, name='search_ban_list'),
    url(r'^banned/kicks/$', views.kicklist, name='admin_kicks'),
    url(r'^banned/last/$', views.penalty_list, name='penalty_list'),
    url(r'^banned/notices/$', views.notice_list, name='notice_list'),
    url(r'^banned/$', views.banlist, name='ban_list'),
)