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

from rconconsole.q3a.games.q3a import Q3ARcon
import re
import threading
import time

class Iourt41(Q3ARcon):

    _gametype = {'0': 'ffa',
                 '3': 'tdm',
                 '4': 'ts',
                 '5': 'ftl',
                 '6': 'cah',
                 '7': 'ctf',
                 '8': 'bomb'}

    _gametype_set = {'ffa': '0',
                     'tdm': '3',
                     'ts': '4',
                     'ftl': '5',
                     'cah': '6',
                     'ctf': '7',
                     'bomb': '8'}

    _regPlayer = re.compile(r'^(?P<slot>[0-9]+)\s+(?P<score>[0-9-]+)\s+(?P<ping>[0-9]+|CNCT|ZMBI)\s+(?P<name>.*?)\s+(?P<last>[0-9]+)\s+(?P<ip>[0-9.]+):(?P<port>[0-9-]+)\s+(?P<qport>[0-9]+)\s+(?P<rate>[0-9]+)$', re.I)
    _reColor = re.compile(r'(\^.)|[\x00-\x20]|[\x7E-\xff]')
    
    def __init__(self, host, password):
        super(Iourt41, self).__init__(host, password)
        self._commands['saybig'] = 'bigtext "%(message)s"'
        self._commands['cyclemap'] = 'cyclemap'
        self._commands['slap'] = 'slap %(cid)s'
        self._commands['nuke'] = 'nuke %(cid)s'
        self._commands['mute'] = 'mute %(cid)s'
        self._commands['set'] = '%(name)s "%(value)s"'

    def getGametype(self):
        value = super(Iourt41, self).getGametype()
        if value:
            return self._gametype.get(value, None)
        return None
    
    def setGametype(self, value):
        data = self._gametype_set.get(value, None)
        if data:
            return super(Iourt41, self).setGametype(data)
        return None
    
    def saybig(self, msg):
        return self.output.write(self.getCommand('saybig', message=msg))

    def slap(self, cid):
        return self.output.write(self.getCommand('slap', cid=cid))

    def nuke(self, cid):
        return self.output.write(self.getCommand('nuke', cid=cid))

    def mute(self, cid):
        return self.output.write(self.getCommand('mute', cid=cid))
                                
    def unban(self, ip):
        r = super(Iourt41, self).unban(ip);
        t1 = threading.Timer(1, self._unbanmultiple, (ip,))
        t1.start()
        return r

    def _unbanmultiple(self, ip):
        # UrT adds multiple instances to banlist.txt Make sure we remove up to 4 remaining duplicates in a separate thread
        for i in range(0,4):
            self.write(self.getCommand('unban', ip=ip))
            time.sleep(2)
            
            