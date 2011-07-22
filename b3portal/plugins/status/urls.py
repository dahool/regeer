# -*- coding: utf-8 -*-
"""Copyright (c) 2011 Sergio Gabriel Teves
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
    url(r'^$', views.game_status, name='home'),
    url(r'^players/$', views.player_chart, name='players_status_chart'),
    url(r'^player/detail/(?P<id>[0-9]+)/$', views.client_detail, name='client_log'),
)