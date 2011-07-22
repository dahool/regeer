# -*- coding: utf-8 -*-
"""Copyright (c) 2009 Sergio Gabriel Teves
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
from django.template import Variable, Library
import datetime

register = Library()

def timesincesec(value, arg=None):
    """Formats a date as the time since that date with minimun value as seconds (i.e. "4 days, 6 hours")."""
    from common.utils.timesince import timesince
    if not value:
        return u''
    try:
        if arg:
            return timesince(value, arg)
        return timesince(value)
    except (ValueError, TypeError):
        return u''
timesincesec.is_safe = False
register.filter(timesincesec)

def summinutes(value, min):
    v = datetime.timedelta(minutes=min)
    return value + v
register.filter(summinutes)