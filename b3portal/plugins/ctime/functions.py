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

from b3portal.plugins.ctime.models import ClientTime
import datetime

def get_total_playtime(client):
    """
    Returns the total played time in seconds.
    Result:
    Dict: 'since': first appearance
          'total': total time in seconds
    """
    total = 0
    clist = client.playtime.all().order_by('id')
    first = datetime.datetime.fromtimestamp(long(clist[0].start))
    for ctime in clist:
        total += long(ctime.end) - long(ctime.start)
    return {'since': first, 'total': total}
    