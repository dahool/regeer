from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^penalty/add/(?P<id>[0-9]+)/$', views.addpenalty, name='add_penalty'),
    url(r'^penalty/disable/(?P<id>[0-9]+)/$', views.disablepenalty, name='disable_penalty'),
    url(r'^penalty/edit/(?P<id>[0-9]+)/$', views.editpenalty, name='edit_penalty'),
    url(r'^notice/add/(?P<id>[0-9]+)/$', views.addpenalty, name='add_notice', kwargs={'notice': True}),
    url(r'^group/update/(?P<id>[0-9]+)/$', views.change_clientgroup, name='change_clientgroup'),
    url(r'^detail/(?P<id>[0-9]+)/$', views.client, name='client_detail'),
    url(r'^inactive/admins/$', views.adminlist, name='inactive_admin_list', kwargs={'filter': True}),
    url(r'^admin/$', views.adminlist, name='admin_list'),
    url(r'^map/$', views.player_map, name='world_map'),
    url(r'^redirect/$', views.direct, name='go_player'),
    url(r'^regular/$', views.regularclients, name='regularclient_list'),
    url(r'^more/(?P<id>[0-9]+)/aliases/$', views.more_alias, name='client_more_alias'),
    url(r'^more/(?P<id>[0-9]+)/admactions/$', views.more_admactions, name='client_more_admactions'),
    url(r'^more/(?P<id>[0-9]+)/ipenalties/$', views.more_ipenalties, name='client_more_ipenalties'),
    url(r'^more/(?P<id>[0-9]+)/notices/$', views.more_notices, name='client_more_notices'),
    url(r'^$', views.clientlist, name='client_list'),
)