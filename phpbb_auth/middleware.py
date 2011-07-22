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
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from phpbb_auth.models import bbUser, bbSession, bbSessionKey
from django.contrib import auth
from django.contrib.auth.models import User
import hashlib
from django.http import HttpResponseRedirect

def is_validSession(user_id, session_id, session_key, request):
    try:
        session = bbSession.objects.get(session_id=session_id,
                                        session_user_id=user_id,
                                        session_ip=request.META["REMOTE_ADDR"])
    except:
        # it is supposed to be only 1 valid session
        return False

    if session:
        return True
#    
#        key = hashlib.md5(session_key).hexdigest()
#        try:
#            sessionkey = bbSessionKey.objects.get(key_id=key,
#                                                  user_id=user_id,
#                                                  last_ip=request.META["REMOTE_ADDR"])
#        except:
#            return False
#        
#        if sessionkey:
#            return True
        
    return False

class bbRemoteUserMiddleware(object):
    """
    Middleware for utilizing phpbb authentication.

    If phpbb cookies exists, the users is automatically logged
    using phpbb session data
    
    phpbb cookie name must be declared in settings PHPBB_COOKIE_NAME
    """
    
    COOKIE_PREFIX = getattr(settings, 'PHPBB_COOKIE_NAME', 'phpbb_')
    
    def logout(self, request):
        auth.logout(request)
        #return HttpResponseRedirect(settings.LOGIN_URL)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    
    def get_cookie(self, request, key):
        try:
            return request.COOKIES['%s_%s' % (self.COOKIE_PREFIX, key)]
        except:
            return None
        
    def process_request(self, request):
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The phpbb remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the bbRemoteUserMiddleware class.")

        c_session_key = None
        c_user_id = self.get_cookie(request, 'u')
        c_session_id = self.get_cookie(request, 'sid')
        d_session_key = self.get_cookie(request, 'd')

        if c_session_id is not None and c_session_id == d_session_key:
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
            if not hasattr(request.user, '_phpbb_user_cache'):
                try:
                    bbuser = bbUser.objects.get(username=request.user.username)
                except bbUser.DoesNotExist:
                    return self.logout(request)
                request.user._phpbb_user_cache = bbuser
            # is the cookie user the same authenticated user ?
            if request.user._phpbb_user_cache.user_id == c_user_id:
                return
            self.logout(request)
            
        if is_validSession(c_user_id, c_session_id, c_session_key, request):
            # User is valid.  Set request.user and persist user in the session
            try:
                bbuser = bbUser.objects.get(user_id=c_user_id)
                user = User.objects.get(username=bbuser.username)
            except (User.DoesNotExist, bbUser.DoesNotExist):
                # if django user do not exists we will force
                # the user to reauthenticate the first time
                return self.logout(request)
            user.backend = 'phpbb_auth.backends.phpbbBackend'
            request.user = user
            auth.login(request, user)
        else:
            return self.logout(request)
        
    def process_response(self, request, response):
        if response:
            try:
                c_session_id = request.COOKIES['%s_sid' % self.COOKIE_PREFIX]
                response.set_cookie('%s_d' % self.COOKIE_PREFIX, c_session_id)
            except:
                pass
        return response