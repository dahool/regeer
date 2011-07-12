from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^$', views.game_status, name='game_status'),
    url(r'^players/$', views.player_chart, name='players_status_chart'),
    url(r'^player/detail/(?P<id>[0-9]+)/$', views.client_detail, name='client_status_log'),
)