# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from common.view.i18n import set_language
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'b3portal.views.home', name='home'),
    url('^admin/', include(admin.site.urls)),
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
        
#if 'plugins.stats' in settings.INSTALLED_APPS:
#    urlpatterns += patterns('',
#        url('^stats/', include('plugins.stats.urls')),
#    )
#
#if 'plugins.follow' in settings.INSTALLED_APPS:
#    urlpatterns += patterns('',
#        url('^follow/', include('plugins.follow.urls')),
#    )
#
#if 'plugins.chatlog' in settings.INSTALLED_APPS:
#    urlpatterns += patterns('',
#        url('^log/', include('plugins.chatlog.urls')),
#    )
#        
#if 'plugins.chatlog' in settings.INSTALLED_APPS:
#    urlpatterns += patterns('',
#        url('^log/', include('plugins.chatlog.urls')),
#    )
            
urlpatterns += staticfiles_urlpatterns()

#if settings.STATIC_SERVE:
#    urlpatterns += patterns('',
#        (r'^webmedia/(?P<path>.*)$', 'django.views.static.serve',
#         {'document_root': settings.MEDIA_ROOT}),
#    )