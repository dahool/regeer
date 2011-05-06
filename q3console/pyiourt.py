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
from pyquake3 import PyQuake3

class Player(object):
    def __init__(self, slot, score, ping, name, ip):
        self.slot = slot
        self.score = score
        self.ping = ping
        self.name = name
        self.ip = ip
    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self)
    
class PyIoUrt(PyQuake3):
    
    # this regex do not match bots. wich is ok.
    _regPlayer = re.compile(r'^(?P<slot>[0-9]+)\s+(?P<score>[0-9-]+)\s+(?P<ping>[0-9]+|CNCT|ZMBI)\s+(?P<name>.*?)\s+(?P<last>[0-9]+)\s+(?P<ip>[0-9.]+):(?P<port>[0-9-]+)\s+(?P<qport>[0-9]+)\s+(?P<rate>[0-9]+)$', re.I)
    _regColor = re.compile(r'\^[0-9]')
    
#    def parse_players(self, data):
#        pass
    
    def rcon_update(self):
        cmd, data = self.rcon('status')
        self.players = []
        for line in data.split('\n')[3:]:
            m = re.match(self._regPlayer, line.strip())
            if m:
                self.players.append(Player(m.group('slot'),
                                           m.group('score'),
                                           m.group('ping'),
                                           self._regColor.sub('',m.group('name')),
                                           m.group('ip')))
