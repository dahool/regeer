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
from django.contrib import admin
#from b3connect.admin import CustomModelAdmin
from models import ChatLog
from django.http import HttpResponseRedirect

from b3portal.plugins.chatlog.models import ChatLogPlugin

# class ChatAdmin(CustomModelAdmin):
#     search_fields=['=client__id','client__name', 'message']
#     list_display=('client', 'message', 'time_add', 'target')
#     list_filter=('time_add',)
#     
#     def get_urls(self):
#         from django.conf.urls.defaults import patterns
#         urls = super(ChatAdmin, self).get_urls()
#         my_urls = patterns('',
#             (r'^filter/$', self.admin_site.admin_view(self.filter))
#         )
#         return my_urls + urls
#         
#     def filter(self, request):
#         import datetime
#         from time import mktime
#         import urllib
#         from django.core.urlresolvers import reverse
#         info = self.model._meta.app_label, self.model._meta.module_name
#         
#         format = "%Y-%m-%d %H:%M:%S"
#         since = datetime.datetime.strptime("%s %s" % (request.GET['time_add_f0'], request.GET['time_add_f1']), format)
#         until = datetime.datetime.strptime("%s %s" % (request.GET['time_add_t0'], request.GET['time_add_t1']), format)
# 
#         url = urllib.urlencode({'time_add__gte': str(int(mktime(since.timetuple()))),
#                                 'time_add__lte': str(int(mktime(until.timetuple())))
#                                 })
#         
#         return HttpResponseRedirect(reverse('admin:%s_%s_changelist' % info) + "?%s" % url)
    
#admin.site.register(ChatLog, ChatAdmin)
admin.site.register(ChatLogPlugin)
