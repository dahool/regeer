# -*- coding: utf-8 -*-
"""Copyright (c) 2012 Sergio Gabriel Teves
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

from django.conf import settings
import datetime
import time
from django.utils.dateformat import format
from django.db.models import Sum
from django.core.cache import cache

def format_date(ts, fmt=settings.SHORT_DATE_FORMAT):
    if not isinstance(ts, datetime.datetime):
        ts = datetime.datetime.fromtimestamp(ts)
    return format(ts, fmt)

def seconds_from_midnight(d):
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime.fromtimestamp(d)
    dt = datetime.datetime.strptime('2012-01-01 %s:%s' % (d.hour, d.minute),'%Y-%m-%d %H:%M')
    midNight = datetime.datetime(2012,1,1,0,0)
    return (dt - midNight).seconds
    
def get_player_activity(client):
    """
    Player activity
    returns an array of tuple with format [(index, date, start, end),]
    """
    clist = client.playtime.all().order_by('id')
    data = []
    limit = 31
    d = {}
    idx = 1
    for ctime in clist:
        if format_date(ctime.start) == format_date(ctime.end):
            start = seconds_from_midnight(ctime.start)
            end = start + (ctime.end - ctime.start)            
            d1 = datetime.datetime.fromtimestamp(ctime.start)
            if not d.has_key(format_date(d1)):
                d[format_date(d1)] = idx
                idx+=1
            data.append([d[format_date(d1)]-1, format_date(d1), start, end])
        else:
            start = seconds_from_midnight(ctime.start)
            end = start + (86400 - start) 
            d1 = datetime.datetime.fromtimestamp(ctime.start)
            if not d.has_key(format_date(d1)):
                d[format_date(d1)] = idx
                idx+=1
            data.append([d[format_date(d1)]-1, format_date(d1), start, end])
            if idx == limit: break;
            start = 0
            end = seconds_from_midnight(ctime.end)            
            d1 = datetime.datetime.fromtimestamp(ctime.end)
            if not d.has_key(format_date(d1)):
                d[format_date(d1)] = idx
                idx+=1
            data.append([d[format_date(d1)]-1, format_date(d1), start, end])
        if idx == limit: break;
    return data

def get_total_playtime(client, key, days = None, cached = True):
    """
    Returns the total played time in seconds.
    Result:
    Dict: 'since': first appearance
          'total': total time in seconds
    """
    ckey = "act-%s-%s+%s" % (str(client.pk), str(key), str(days) if days is not None else '0')
    response = None
    if cached: response = cache.get(ckey)
    if not response:
        if days:
            since = datetime.datetime.now() - datetime.timedelta(days=days)
            q = client.playtime.filter(came__gte=time.mktime(since.timetuple()))
        else:
            q = client.playtime.all()
        first = datetime.datetime.fromtimestamp(q.order_by('id')[0].start)
        sums = q.aggregate(Sum('came'), Sum('gone'))
        total = (sums['gone__sum'] - sums['came__sum']) * 60
        response = {'since': first, 'total': total}
        cache.set(ckey, response, getattr(settings, 'ACTIVITY_CACHE', 120)*60) 
    return response