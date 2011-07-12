import datetime
import xml.dom.minidom

UP_TIME_FORMAT= '%a %b %d %H:%M:%S %Y'

_gametype_detail = {'ffa': 'Free For All',
                 'tdm': 'Team Death Match',
                 'ts': 'Team Survivor',
                 'ftl': 'Follow The Leader',
                 'cah': 'Capture And Hold',
                 'ctf': 'Capture The Flag',
                 'bomb': 'Bomb',
                 'bm': 'Bomb'}

class Client(object):
    name = None
    team = None
    id = None
    ip = None
    guid = None
    cid = None
    updated = None
    score = 0
    
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
    round = 0
    state = 0
    password = None
    
    def __init__(self, xmlfile):
        self.clients = []
        doc = xml.dom.minidom.parse(xmlfile)
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
                        self.blueTeamName = value
                    elif name == 'g_teamnamered':
                        self.redTeamName = value
    
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
    