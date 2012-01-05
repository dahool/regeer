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
from b3portal.plugins import PLUGINS
from b3portal.plugins import is_plugin_installed
from django.conf import settings

import views

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^client/', include('b3portal.client.urls')),
    url(r'^banned/', include('b3portal.penalties.urls')),
)

if settings.B3_INSTALLED:
    urlpatterns += patterns('',
        url(r'^rcon/', include('b3portal.rconadmin.urls')),
    )    

for plugin in PLUGINS:
    if is_plugin_installed(plugin[0]):
        app = plugin[0]
        urlpatterns += patterns('',
            url(r'^%s/' % app, include("b3portal.plugins.%s.urls" % app, namespace=app))
        )