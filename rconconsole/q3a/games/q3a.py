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
    _statusExpire = 30
       
    def __init__(self, host, password):
        self.output = Rcon(host, password)
    
    def write(self, *args):
        '''write to console
        args: anything
        '''        
        return self.output.write(args[0])
    
    def getStatus(self):
        if self._status and self._lastStatus + self._statusExpire > time.time():
            return self._status
        data = self.write('status')
        if data:
            self._status = data
            self._lastStatus = time.time()
        return data
          
    def getClients(self, *args):
        """get client list
        args: None
        """
        data = self.getStatus()
        if not data:
            return []
        
        status = []
        for line in data.split('\n'):
            m = self._regPlayer.match(line.strip())
            if not m:
                m = self._regPlayerShort.match(line.strip())
            
            if m:
                p = Player()
                p.cid = m.group('slot')
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
    
    def getMap(self, *args):
        """get current map name
        args: None
        """
        data = self.getStatus()
        if not data:
            return None
        line = data.split('\n')[0]
        m = re.match(self._reMapNameFromStatus, line.strip())
        if m:
            return str(m.group('map'))
        return None

    def getHostname(self, *args):
        '''get hostname
        args: None
        '''
        return self.getCvar(self.getCommand('hostname'))
          
    def setHostname(self, *args):
        '''set hostname
        args: new name
        '''        
        self.setCvar(self.getCommand('hostname'), args[0])
        
    def getNextMap(self, *args):
        '''get nextmap
        args: None
        '''        
        return self.getCvar(self.getCommand('nextmap'))

    def setNextMap(self, *args):
        '''set nextmap
        args: map name
        '''        
        self.setCvar(self.getCommand('nextmap'), args[0])
    
    def getPassword(self, *args):
        '''get password
        args: None
        '''        
        return self.getCvar(self.getCommand('password'))
    
    def setPassword(self, *args):
        '''set password
        args: new password
        '''        
        self.setCvar(self.getCommand('password'), args[0])

    def getGametype(self, *args):
        '''get gametype
        args: None
        '''        
        return self.getCvar(self.getCommand('gametype'))

    def setGametype(self, *args):
        '''set gametype
        args: gametype
        '''        
        self.setCvar(self.getCommand('gametype'), args[0])
    
    def getCvar(self, *args):
        '''get cvar
        args: cvar name
        '''        
        m = None
        if self._reCvarName.match(args[0]):
            val = self.write(args[0])
            for f in self._reCvar:
                m = re.match(f, val)
                if m:
                    break            
            if m:
                if m.group('cvar').lower() == args[0].lower():
                    try:
                        default_value = m.group('default')
                    except IndexError:
                        default_value = None
                    return (m.group('cvar'), m.group('value'), default_value)
            else:
                return None
            
    def setCvar(self, *args):
        '''set cvar
        args: name, value
        '''        
        if self._reCvarName.match(args[0]):
            self.write(self.getCommand('set', name=args[0], value=args[1]))

    def say(self, *args):
        """print message to console
        args: message
        """
        return self.write(self.getCommand('say', message=args[0]))

    def message(self, *args):
        """send a message to a player
        args: cid, text
        """
        return self.write(self.getCommand('message', cid=args[0], message=args[1]))
        
    def ban(self, *args):
        """add ip to server banlist
        args: ip
        """
        return self.write(self.getCommand('ban', cid=args[0]))

    def unban(self, *args):
        """remove a ip from banlist
        args: ip
        """
        return self.write(self.getCommand('unban', ip=args[0]))

    def kick(self, *args):
        """kick given player
        args: cid
        """
        return self.write(self.getCommand('kick', cid=args[0]))

    def rotateMap(self, *args):
        """cycle to next map
        args: None
        """
        return self.write(self.getCommand('cyclemap'))

    def changeMap(self, *args):
        """change current map
        args: map name
        """
        return self.write(self.getCommand('map', map=args[0]))

    def getCommand(self, cmd, **kwargs):
        """Return a reference to a loaded command"""
        try:
            cmd = self._commands[cmd]
        except KeyError:
            return None
        return cmd % kwargs            
