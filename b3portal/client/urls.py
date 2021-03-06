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
    url(r'^notice/del/(?P<id>[0-9]+)/$', views.removenotice, name='del_notice'),
    url(r'^note/add/(?P<id>[0-9]+)/$', views.addnote, name='add_note'),
    url(r'^note/del/(?P<id>[0-9]+)/$', views.removenotice, name='del_note'),
    url(r'^group/update/(?P<id>[0-9]+)/$', views.change_clientgroup, name='change_clientgroup'),
    url(r'^detail/(?P<id>[0-9]+)/$', views.client, name='client_detail'),
    url(r'^detail/(?P<id>[0-9]+)/penalties/$', views.client_penalty_detail, name='client_detail_penalties'),
    url(r'^detail/(?P<id>[0-9]+)/activity/$', views.client_activity_detail, name='client_detail_activity'),
    url(r'^admin/inactive/$', views.adminlist, name='inactive_admin_list', kwargs={'filter': True}),
    url(r'^admin/$', views.adminlist, name='admin_list'),
    url(r'^map/$', views.player_map, name='world_map'),
    url(r'^redirect/$', views.direct, name='go_player'),
    url(r'^regular/$', views.regularclients, name='regularclient_list'),
    url(r'^more/(?P<id>[0-9]+)/aliases/$', views.more_alias, name='client_more_alias'),
    url(r'^more/(?P<id>[0-9]+)/ipaliases/$', views.more_ipalias, name='client_more_ipalias'),
    url(r'^more/(?P<id>[0-9]+)/admactions/$', views.more_admactions, name='client_more_admactions'),
    url(r'^more/(?P<id>[0-9]+)/penalties/$', views.more_penalties, name='client_more_penalties'),
    url(r'^more/(?P<id>[0-9]+)/ipenalties/$', views.more_ipenalties, name='client_more_ipenalties'),
    url(r'^more/(?P<id>[0-9]+)/notices/$', views.more_notices, name='client_more_notices'),
    url(r'^more/(?P<id>[0-9]+)/logs/$', views.more_logs, name='client_more_logs'),
    url(r'^more/(?P<id>[0-9]+)/notes/$', views.more_notes, name='client_more_notes'),
    url(r'^group/list/(?P<id>[0-9]+)/$', views.group_list, name='list_groups'),
    url(r'^$', views.clientlist, name='client_list'),
)