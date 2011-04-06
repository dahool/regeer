# -*- coding: utf-8 -*-
import logging
import time
import sys

import b3
import b3.game
import b3.clients
from b3.parsers.iourt41 import Iourt41Parser

class DummyHandler(logging.Handler):
    """
  A handler class which ignores all.
    """
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        pass

    def close(self):
        logging.Handler.close(self)

def getLoggerInstance():
    logging.setLoggerClass(b3.output.OutputHandler)
    log = logging.getLogger('output')
    handler = DummyHandler()
    log.addHandler(handler)
    return log
    
class B3Console(Iourt41Parser):

    def __init__(self, config):
        self.config = config
        self.log = getLoggerInstance()

        #sys.stdout = b3.output.stdoutLogger(self.log)
        #sys.stderr = b3.output.stderrLogger(self.log)

        bot_prefix = self.config.get('b3', 'bot_prefix')
        if bot_prefix:
            self.prefix = bot_prefix

        self.msgPrefix = self.prefix
        
        self._rconIp   = self.config.get('server', 'rcon_ip')
        self._port     = self.config.getint('server', 'port')
        self.output = self.OutputClass(self, (self._rconIp, self._port),self.config.get('server', 'rcon_password'))
        
        self.game = b3.game.Game(self, None)
        map = self.getMap()
        if map:
            self.game.mapName = map
        
    def __del__(self):
        self.output.close()
        
class B3Client(object):

    _gametype = {'ffa': 0,
                 'tdm': 3,
                 'ts': 4,
                 'ftl': 5,
                 'cah': 6,
                 'ctf': 7,
                 'bomb': 8}

    _gametype_detail = {'ffa': 'Free For All',
                 'tdm': 'Team Death Match',
                 'ts': 'Team Survivor',
                 'ftl': 'Follow The Leader',
                 'cah': 'Capture And Hold',
                 'ctf': 'Capture The Flag',
                 'bomb': 'Bomb'}
    
    def __init__(self, configFile):
        self.console = B3Console(b3.config.load(configFile))
        self.console.game.fs_game = self.console.getCvar('fs_game').getString()
        self.console.game.fs_basepath = self.console.getCvar('fs_basepath').getString().rstrip('/')
        self.console.game.fs_homepath = self.console.getCvar('fs_homepath').getString().rstrip('/')
        
    def getservername(self):
        res = self.console.getCvar("sv_hostname")
        if res is not None:
            res = res.getString()
        return res
        
    def _normalize(self, data):
        return data.encode('utf_8').strip()
    
    def map(self, data, action):
        if action=="get":
            data = "Current map: %s" % self.console.getMap()
        else:
            self.bigtext('Changing map to %s' % data)
            time.sleep(1)
            self.console.write('map %s' % self._normalize(data))
            time.sleep(5)
            data = "Map changed to: %s" % data
        return data        
    
    def nextmap(self, data, action):
        if action=="get":
            data = "Next map is: %s" % self.console.getNextMap()
        else:
            self.console.write('g_nextmap "%s"' % self._normalize(data))
            data = "Next map set to: %s" % data
        return data
        
    def cyclemap(self, data=None, action=None):
        nextmap = self.console.getNextMap()
        self.bigtext('Cycling map')
        time.sleep(1)
        self.console.write('cyclemap')
        return "Map cycled to %s" % nextmap

    def restartmap(self, data=None, action=None):
        self.console.write('restart')
        self.console.say('^7Map restarted')
        return "Map restarted"
    
    def reloadmap(self, data=None, action=None):
        self.bigtext('^7Reloading map')
        time.sleep(1)
        self.console.write('reload')
        return "Map reloaded"

    def bigtext(self, data, action=None):
        self.console.write( 'bigtext "^7%s"' % self._normalize(data))
        return 'Done bigtext'

    def scream(self, data, action=None):
        text = self._normalize(data)
        for i in range(1,5):
            self.console.say('^%d%s' % (i,text))
            time.sleep(1)
        return 'Done scream'
        
    def say(self, data, action=None):
        self.console.say('^7%s' % self._normalize(data))
        return 'Done say'
        
    def password(self, data, action):
        if action=="get":
            p = self.console.getCvar('g_password')
            if p is None:
                data = ''
            else:
                data = p.getString()
            return "Current server password: %s" % data
        else:
            if len(data)>0:
                self.console.setCvar( 'g_password', '' )
                self.console.say('^7public mode: ^2ON')
                return "public mode: ON"
            else:
                self.console.setCvar( 'g_password', '%s' % self._normalize(data))
                self.console.say('^7public mode: ^9OFF')
                self.bigtext('^7Server going ^3PRIVATE^7 soon !!')
                time.sleep(1)
                self.bigtext('^3Server going ^7PRIVATE^3 soon !!')
                return "public mode: OFF"
                    
    def gametype(self, data, action):
        if action=="get":
            i = self.console.getCvar('g_gametype').getInt()
            if i == 0:
                t = 'ffa'
            elif i == 8:
                t = 'bomb'
            else:
                t = self.console.defineGameType(str(i))
            return self._gametype_detail[t]
        else:
            new_type = self._gametype[data]
            new_type_det = self._gametype_detail[data]
            self.console.write('g_gametype %d' % new_type)
            self.bigtext('^7Next game is ^3%s' % new_type_det)
            self.console.say('"^7Next game is ^3%s"' % new_type_det)
        return "Game type changed to: %s" % new_type_det

    def write(self, data, action=None):
        v = self.console.write(self._normalize(data))
        if v:
            return '%s => %s' % (data,getattr(v, 'getString', v))
        return data

    def cvar(self, data, action):
        if action=="get":
            v = self.console.getCvar("%s" % self._normalize(data))
            if v:
                return '%s => %s' % (data,v.getString())
            else:
                return 'Error (%s)' % data
        else:
            k,v = self._normalize(data).split(' ')
            self.console.setCvar(k,v)
            return '%s => %s' % (k,v)
        
    def kick(self, data, action=None):
        cid = self._normalize(data)
        self.console.kick(cid, 'kicked by GOD')
        return 'Client kicked'        