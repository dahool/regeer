# -*- coding: UTF-8 -*-
"""Copyright (c) 2012, Sergio Gabriel Teves
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
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User, Permission
from phpbb_auth.models import bbUser

class Command(BaseCommand):

    args = '<username>'
    help = 'Migrate an existing phpbb user'
    
    def handle(self, *args, **options):
        if not args:
            self.stdout.write('Please, enter username')
        else:
            username = args[0]
            try:
                user = bbUser.objects.get(username_clean=username.lower())
            except bbUser.DoesNotExist, e:
                raise CommandError(str(e))
            try:
                localuser = User.objects.get(username=username)
            except User.DoesNotExist:
                localuser = User.objects.create(username=username,
                                                email=user.user_email)
                localuser.set_unusable_password()
                localuser.save()
                self.stdout.write('Done.\n')
            else:
                self.stdout.write('User already exists')
