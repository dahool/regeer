# -*- coding: utf-8 -*-
from django.contrib import admin
from b3connect.admin import CustomModelAdmin
from models import ChatLog
from django.http import HttpResponseRedirect

from b3portal.plugins.chatlog.models import ChatLogPlugin

class ChatAdmin(CustomModelAdmin):
    search_fields=['=client__id','client__name', 'data']
    list_display=('client', 'data', 'time_add', 'target')
    list_filter=('time_add',)
    
    def get_urls(self):
        from django.conf.urls.defaults import patterns
        urls = super(ChatAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^filter/$', self.admin_site.admin_view(self.filter))
        )
        return my_urls + urls
        
    def filter(self, request):
        import datetime
        from time import mktime
        import urllib
        from django.core.urlresolvers import reverse
        info = self.model._meta.app_label, self.model._meta.module_name
        
        format = "%Y-%m-%d %H:%M:%S"
        since = datetime.datetime.strptime("%s %s" % (request.GET['time_add_f0'], request.GET['time_add_f1']), format)
        until = datetime.datetime.strptime("%s %s" % (request.GET['time_add_t0'], request.GET['time_add_t1']), format)

        url = urllib.urlencode({'time_add__gte': str(int(mktime(since.timetuple()))),
                                'time_add__lte': str(int(mktime(until.timetuple())))
                                })
        
        return HttpResponseRedirect(reverse('admin:%s_%s_changelist' % info) + "?%s" % url)
    
#admin.site.register(ChatLog, ChatAdmin)
admin.site.register(ChatLogPlugin)