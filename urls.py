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
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from common.view.i18n import set_language
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'b3portal.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^login/$', auth_views.login, kwargs={'template_name':'auth/login.html'}, name='user_signin'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/' }, name='auth_logout'),
    url('^', include('b3portal.urls')),
    #url(r'^setlang/$', 'django.views.i18n.set_language', name='set_lang'),
)

for app in settings.INSTALLED_APPS:
    if app.startswith('plugins.'):
        p, name = app.split('.')
        pattern = '^%s/' % name
        urlconf = '%s.urls' % app
        urlpatterns += patterns('',
            url(pattern, include(urlconf)),
        )
             
urlpatterns += staticfiles_urlpatterns()