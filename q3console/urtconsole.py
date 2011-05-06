# -*- coding: utf-8 -*-
"""Copyright (c) 2011, Sergio Gabriel Teves
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

import re
from pyiourt import PyIoUrt as Console
    
class UrtClient(object):

    color_re = re.compile(r'\^[0-9]')

    _gametype = {'0': 'ffa',
                 '3': 'tdm',
                 '4': 'ts',
                 '5': 'ftl',
                 '6': 'cah',
                 '7': 'ctf',
                 '8': 'bomb'}
    
    _gametype_rev = {'ffa': '0',
                 'tdm': '3',
                 'ts': '4',
                 'ftl': '5',
                 'cah': '6',
                 'ctf': '7',
                 'bomb': '8'}
    
    def __init__(self, host, rconpassword):
        self.host = host
        self.rconpassword = rconpassword
        self.console = Console(host, rconpassword)
        self.players = None
        # test connection
        self.console.update()
        
    def check_rcon(self):
        """
        check if rcon password is valid
        """
        try:
            self.console.rcon('status')
        except:
            return False
        return True

    def getservername(self):
        return self.get_cvar("sv_hostname")
        
    def get_player_list(self, force = False):
        if self.players and not force:
            return self.players
        self.console.rcon_update()
        self.players = self.console.players 
        return self.players
    
    def _clean_colors(self, text):
        if text:
            return self.color_re.sub('',text)
        return text
        
    def _normalize(self, data):
        if data:
            return data.encode('utf_8').strip()
        return data

    def write(self, data):
        cmd, data = self.console.rcon(self._normalize(data))
        return data
    
    def get_cvar(self, data):
        try:
            return self._clean_colors(self.console.vars[data])
        except IndexError:
            return None

    def set_cvar(self, name, value):
        data = self.write('set %s %s' % (self._normalize(name), self._normalize(value)))
        return data
    
    def cyclemap(self):
        data = self.write('cyclemap')
        return data

    def restartmap(self):
        data = self.write('restart')
        return None
    
    def reloadmap(self):
        data = self.write('reload')
        return data

    def bigtext(self, data):
        data = self.write('bigtext "^7%s"' % data)
        return data

    def say(self, data):
        data = self.write('say "^7%s"' % data)
        return data
                    
    def kick(self, data):
        data = self.write('clientkick %s' % data)
        return data   

    def slap(self, data):
        data = self.write('slap %s' % data)
        return data
        
    def set_map(self, data):
        self.write('map %s' % data)
        
    def get_map(self):
        return self.get_cvar('mapname')

    def set_nextmap(self, data):
        self.set_cvar('g_nextmap', data)
        
    def get_nextmap(self):
        return self.get_cvar('g_nextmap')
    
    def set_password(self, data):
        self.set_cvar('g_password', data)
        
    def get_password(self):
        return self.get_cvar('g_password')
        
    def set_gametype(self, data):
        self.set_cvar('g_gametype', self._gametype_rev[data])
        
    def get_gametype(self):
        c = self.get_cvar('g_gametype')
        if c:
            return self._gametype[c] 
        return 'Unknown'
        
if __name__ == '__main__':
    host = ''
    password = ''
    client = UrtClient(host, password)
    client.set_password('')
