# -*- coding: utf-8 -*-
"""Copyright (c) 2010,2011 Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^penalty/add/(?P<id>[0-9]+)/$', views.addpenalty, name='add_penalty'),
    url(r'^penalty/disable/(?P<id>[0-9]+)/$', views.disablepenalty, name='disable_penalty'),
    url(r'^penalty/edit/(?P<id>[0-9]+)/$', views.editpenalty, name='edit_penalty'),
    url(r'^notice/add/(?P<id>[0-9]+)/$', views.addpenalty, name='add_notice', kwargs={'notice': True}),
    url(r'^group/update/(?P<id>[0-9]+)/$', views.change_clientgroup, name='change_clientgroup'),
    url(r'^detail/(?P<id>[0-9]+)/$', views.client, name='client_detail'),
    url(r'^admin/inactive/$', views.adminlist, name='inactive_admin_list', kwargs={'filter': True}),
    url(r'^admin/$', views.adminlist, name='admin_list'),
    url(r'^map/$', views.player_map, name='world_map'),
    url(r'^redirect/$', views.direct, name='go_player'),
    url(r'^regular/$', views.regularclients, name='regularclient_list'),
    url(r'^more/(?P<id>[0-9]+)/aliases/$', views.more_alias, name='client_more_alias'),
    url(r'^more/(?P<id>[0-9]+)/ipaliases/$', views.more_ipalias, name='client_more_ipalias'),
    url(r'^more/(?P<id>[0-9]+)/admactions/$', views.more_admactions, name='client_more_admactions'),
    url(r'^more/(?P<id>[0-9]+)/ipenalties/$', views.more_ipenalties, name='client_more_ipenalties'),
    url(r'^more/(?P<id>[0-9]+)/notices/$', views.more_notices, name='client_more_notices'),
    url(r'^group-list/$', views.group_list, name='group_list_json'),    
    url(r'^$', views.clientlist, name='client_list'),
)