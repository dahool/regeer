# -*- coding: utf-8 -*-
"""Copyright (c) 2012 Sergio Gabriel Teves
All rights reserved.

Some parts or this code are copyright of Michael "ThorN" Thornton and BigBrotherBot(B3)

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
from rconconsole.q3a.rcon import Rcon
from rconconsole import Player
import time

class Q3ARcon:

    _regPlayer = re.compile(r'^(?P<slot>[0-9]+)\s+(?P<score>[0-9-]+)\s+(?P<ping>[0-9]+)\s+(?P<guid>[0-9a-zA-Z]+)\s+(?P<name>.*?)\s+(?P<last>[0-9]+)\s+(?P<ip>[0-9.]+):(?P<port>[0-9-]+)\s+(?P<qport>[0-9]+)\s+(?P<rate>[0-9]+)$', re.I)
    _regPlayerShort = re.compile(r'\s+(?P<slot>[0-9]+)\s+(?P<score>[0-9]+)\s+(?P<ping>[0-9]+)\s+(?P<name>.*)\^7\s+', re.I)
    _reCvarName = re.compile(r'^[a-z0-9_.]+$', re.I)
    _reMapNameFromStatus = re.compile(r'^map:\s+(?P<map>.+)$', re.I)
    _reCvar = (
        #"sv_maxclients" is:"16^7" default:"8^7"
        #latched: "12"
        re.compile(r'^"(?P<cvar>[a-z0-9_.]+)"\s+is:\s*"(?P<value>.*?)(\^7)?"\s+default:\s*"(?P<default>.*?)(\^7)?"$', re.I | re.M),
        #"g_maxGameClients" is:"0^7", the default
        #latched: "1"
        re.compile(r'^"(?P<cvar>[a-z0-9_.]+)"\s+is:\s*"(?P<default>(?P<value>.*?))(\^7)?",\s+the\sdefault$', re.I | re.M),
        #"mapname" is:"ut4_abbey^7"
        re.compile(r'^"(?P<cvar>[a-z0-9_.]+)"\s+is:\s*"(?P<value>.*?)(\^7)?"$', re.I | re.M),
    )
    
    _commands = {}
    _commands['message'] = 'tell %(cid)s ^8[pm]^7 %(message)s'
    _commands['say'] = 'say %(message)s'
    _commands['set'] = 'set %(name)s "%(value)s"'
    _commands['kick'] = 'clientkick %(cid)s'
    _commands['ban'] = 'addip %(cid)s'
    _commands['map'] = 'map %(map)s'
    _commands['cyclemap'] = 'map_rotate 0'
    _commands['unban'] = 'removeip %(cid)s'
    
    # cvars
    _commands['hostname'] = 'sv_hostname'
    _commands['nextmap'] = 'g_nextmap'
    _commands['gametype'] = 'g_gametype'
    _commands['password'] = 'g_password'
    
    _reColor = re.compile(r'(\^[0-9a-z])|[\x80-\xff]')
    
    _lastStatus = None
    _status = None
    _statusExpire = 60
       
    def __init__(self, host, password):
        self.output = Rcon(host, password)
    
    def write(self, data):
        return self.output.write(data)
    
    def _get_status(self):
        if self._status and self._lastStatus + self._statusExpire > time.time():
            return self._status
        data = self.write('status')
        if data:
            self._status = data
            self._lastStatus = time.time()
        return data
          
    def getClients(self):
        """get client list"""
        data = self._get_status()
        if not data:
            return []
        
        status = []
        for line in data.split('\n'):
            m = self._regPlayer.match(line.strip())
            if not m:
                m = self._regPlayerShort.match(line.strip())
            
            if m:
                p = Player()
                p.slot = m.group('slot')
                p.score = m.group('score')
                p.ip = m.group('ip')
                try:
                    p.ping = int(m.group('ping'))
                except:
                    p.ping = 999                
                p.name = self._reColor.sub('',m.group('name'))
                if m.groupdict().has_key('guid'):
                    p.guid = m.group('guid')
                status.append(p)
    
        return status
    
    def getMap(self):
        """get current map name"""
        data = self._get_status()
        if not data:
            return None
        line = data.split('\n')[0]
        m = re.match(self._reMapNameFromStatus, line.strip())
        if m:
            return str(m.group('map'))
        return None

    def getHostname(self):
        return self.getCvar(self.getCommand('hostname'))
          
    def setHostname(self, value):
        self.setCvar(self.getCommand('hostname'), value)
        
    def getNextMap(self):
        return self.getCvar(self.getCommand('nextmap'))

    def setNextMap(self, value):
        self.setCvar(self.getCommand('nextmap'), value)
    
    def getPassword(self):
        return self.getCvar(self.getCommand('password'))
    
    def setPassword(self, value):
        self.setCvar(self.getCommand('password'), value)

    def getGametype(self):
        return self.getCvar(self.getCommand('gametype'))
    
    def setGametype(self, value):
        self.setCvar(self.getCommand('gametype'), value)
    
    def getCvar(self, name):
        m = None
        if self._reCvarName.match(name):
            val = self.write(name)
            for f in self._reCvar:
                m = re.match(f, val)
                if m:
                    break            
            if m:
                if m.group('cvar').lower() == name.lower():
                    try:
                        default_value = m.group('default')
                    except IndexError:
                        default_value = None
                    return (m.group('cvar'), m.group('value'), default_value)
            else:
                return None
            
    def setCvar(self, name, value):
        if self._reCvarName.match(name):
            self.write(self.getCommand('set', name=name, value=value))

    def say(self, text):
        """print message to console"""
        return self.write(self.getCommand('say', message=text))

    def message(self, cid, text):
        """send a message to a player"""
        return self.write(self.getCommand('message', cid=cid, message=text))
        
    def ban(self, ip):
        """add ip to server banlist"""
        return self.write(self.getCommand('ban', cid=ip))

    def unban(self, ip):
        """remove a ip from banlist"""
        return self.write(self.getCommand('unban', ip=ip))

    def kick(self, cid):
        """kick given player"""
        return self.write(self.getCommand('kick', cid=cid))

    def rotateMap(self):
        """cycle to next map"""
        return self.write(self.getCommand('cyclemap'))

    def changeMap(self, mapname):
        """change current map"""
        return self.write(self.getCommand('map', map=mapname))

    def getCommand(self, cmd, **kwargs):
        """Return a reference to a loaded command"""
        try:
            cmd = self._commands[cmd]
        except KeyError:
            return None
        return cmd % kwargs            