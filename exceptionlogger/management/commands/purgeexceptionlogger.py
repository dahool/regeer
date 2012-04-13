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
from django.core.management.base import BaseCommand
from django.conf import settings
from exceptionlogger.models import ExceptionLog
import datetime

class Command(BaseCommand):
    help = 'Remove Old Exceptions'

    def handle(self, *args, **options):
        days = getattr(settings, 'PURGE_EXCEPTION_DAYS', 30)
        deltime = datetime.datetime.now() - datetime.timedelta(days=days)
         
        self.stdout.write("Cleaning exceptions older than %s ...\n" % deltime)
        
        c=0
        for ex in ExceptionLog.objects.filter(date__lt=deltime):
            c+=1
            ex.delete()

        self.stdout.write('Removed %d.\n' % c)