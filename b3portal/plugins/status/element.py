# -*- coding: utf-8 -*-
"""Copyright (c) 2011-2012 Sergio Gabriel Teves
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
import datetime
import re
import xml.dom.minidom
from django.utils.translation import gettext as _

UP_TIME_FORMAT= '%a %b %d %H:%M:%S %Y'

_gametype_detail = {'ffa': _('Free For All'),
                 'tdm': _('Team Death Match'),
                 'ts': _('Team Survivor'),
                 'ftl': _('Follow The Leader'),
                 'cah': _('Capture And Hold'),
                 'ctf': _('Capture The Flag'),
                 'bomb': _('Bomb'),
                 'bm': _('Bomb')}

_level_name = {'0': _('Guest'),
                 '1': _('User'),
                 '2': _('Regular'),
                 '20': _('Moderator'),
                 '40': _('Admin'),
                 '60': _('Full Admin'),
                 '80': _('Senior Admin'),
                 '100': _('Super Admin')}

class Client(object):
    name = None
    team = None
    id = None
    ip = None
    guid = None
    cid = None
    updated = None
    score = 0
    level = None
    
    @property
    def get_display_group(self):
        if self.level:
            return _level_name.get(self.level, None)
        
class Status(object):
    
    clients = []
    redScore = None
    blueScore = None
    map = ""
    mapStart = None
    totalClients = 0
    updated = None
    timeLimit = None
    type = None
    typeCode = None
    redTeamName = "Red Team"
    blueTeamName = "Blue Team"
    redTeamCount = 0
    blueTeamCount = 0
    specTeamCount = 0
    round = 0
    state = 0
    password = None
    
    _color_re = re.compile(r'\^[0-9]')

    def __init__(self, xmlfile):
        self.clients = []
        doc = xml.dom.minidom.parse(xmlfile)
        xmlfile.close()
        for b3status in doc.getElementsByTagName("B3Status"):
            self.updated = datetime.datetime.strptime(b3status.getAttribute('Time'),UP_TIME_FORMAT)
            for clients in b3status.getElementsByTagName("Clients"):
                self.totalClients = int(clients.getAttribute("Total"))
                for client in clients.getElementsByTagName("Client"):
                    c = Client()
                    c.name = client.getAttribute('Name')
                    c.team = client.getAttribute('Team')
                    c.score = client.getAttribute('Score')
                    c.state = client.getAttribute('State')
                    c.id = client.getAttribute('DBID')
                    c.cid = client.getAttribute('CID')
                    c.guid = client.getAttribute('GUID')
                    c.ip = client.getAttribute('IP')
                    c.level = client.getAttribute('Level')
                    if c.team == "2":
                        self.redTeamCount+=1
                    elif c.team == "3":
                        self.blueTeamCount+=1
                    elif c.team == "1":
                        self.specTeamCount+=1
                    c.updated = datetime.datetime.strptime(client.getAttribute('Updated'),UP_TIME_FORMAT)
                    self.clients.append(c)
            for game in b3status.getElementsByTagName("Game"):
                self.map = game.getAttribute('Map')
                self.timeLimit = game.getAttribute('TimeLimit')
                self.type = _gametype_detail[game.getAttribute('Type')]
                self.typeCode = game.getAttribute('Type')
                self.round = game.getAttribute('Rounds')
                for data in game.getElementsByTagName("Data"):
                    name = data.getAttribute('Name')
                    value = data.getAttribute('Value')
                    if name == '_mapTimeStart':
                        if value<>"None":
                            self.mapStart = datetime.datetime.fromtimestamp(float(value))
                    elif name == 'g_teamScores':
                        if value<>"None":
                            self.redScore, self.blueScore = data.getAttribute('Value').split(":")
                    elif name == 'g_password':
                        if value<>"None":
                            self.password = value
                    elif name == 'g_teamnameblue':
                        self.blueTeamName = self._color_re.sub('',value)
                    elif name == 'g_teamnamered':
                        self.redTeamName = self._color_re.sub('',value)
    
    @property
    def timeleft(self):
        try:
            fin = self.mapStart+datetime.timedelta(minutes=int(self.timeLimit))
            ahora = datetime.datetime.now()
            if ahora > fin:
                seconds = -1*((ahora-fin).seconds) 
            else:
                seconds = (fin-ahora).seconds
            minutes = seconds / 60
            seconds -= 60*minutes
            return "%02d:%02d" % (minutes, seconds)
        except:
            return "--"
        
if __name__ == '__main__':
    import os
    f = os.path.join(os.path.normpath(os.path.abspath(os.path.dirname(__file__))),'..','..','test','status.xml')
    s = Status(f)
    print s.__dict__
    for c in s.clients:
        print c.__dict__
    