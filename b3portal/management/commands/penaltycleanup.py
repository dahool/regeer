# -*- coding: utf-8 -*-
"""Copyright (c) 2010,2011,2012 Sergio Gabriel Teves
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
from b3portal.models import Server
from b3connect.models import Penalty
from django.db.models import Q
import datetime

class Command(BaseCommand):
    help = 'Remove Old Warnings'

    def handle(self, *args, **options):
        
        if not hasattr(settings, 'PENALTY_CLEANUP_DAYS'):
            self.stdout.write("You must define PENALTY_CLEANUP_DAYS settings to use this function\n")
            return
        
        deltime = datetime.datetime.now() - datetime.timedelta(days=settings.PENALTY_CLEANUP_DAYS)
         
        self.stdout.write("Cleaning warnings and kicks older than %s ...\n" % deltime)
        
        for server in Server.objects.all():
            self.stdout.write("Processing %s ...\n" % server.name)
            q = Penalty.objects.using(server.pk).filter(Q(type='Warning') | Q(type='Kick'),time_add__lt=deltime)
            c = q.count()
            q.delete()
            self.stdout.write("Removed %s ...\n" % c)

        self.stdout.write('Success.\n')