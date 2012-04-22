#
# BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2005 Michael "ThorN" Thornton
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

__author__ = 'ThorN'
__version__ = '1.5'

import socket
import select
import re
import time
import thread
import threading
import Queue
import logging

logger = logging.getLogger('regeer')

#--------------------------------------------------------------------------------------------------
class Rcon:
    host = ()
    password = None
    lock = thread.allocate_lock()
    socket = None
    queue = None
    socket_timeout = 0.80
    rconsendstring = '\377\377\377\377rcon "%s" %s\n'
    rconreplystring = '\377\377\377\377print\n'
    qserversendstring = '\377\377\377\377%s\n'

    encoding = 'latin-1'

    def __init__(self, host, password):
        self.queue = Queue.Queue()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.password = password
        self.socket.settimeout(2)
        self.socket.connect(self.host)

        self._stopEvent = threading.Event()
        thread.start_new_thread(self._writelines, ())

    def encode_data(self, data, source):
        try:
            if isinstance(data, str):
                data=unicode(data, errors='ignore')
            data=data.encode(self.encoding, 'replace')
        except Exception, msg:
            logger.warning('%s: ERROR encoding data: %r', source, msg)
            data = '%s: ERROR encoding data: %r', source, msg
            
        return data
        
    def send(self, data, maxRetries=None, socketTimeout=None):
        if socketTimeout is None:
            socketTimeout = self.socket_timeout
        if maxRetries is None:
            maxRetries = 2

        data = data.strip()
        # encode the data
        if self.encoding:
            data = self.encode_data(data, 'QSERVER')

        logger.debug('QSERVER sending (%s:%s) %r', self.host[0], self.host[1], data)
        startTime = time.time()

        retries = 0
        while time.time() - startTime < 5:
            readables, writeables, errors = select.select([], [self.socket], [self.socket], socketTimeout)

            if len(errors) > 0:
                logger.warning('QSERVER: %r', errors)
            elif len(writeables) > 0:
                try:
                    writeables[0].send(self.qserversendstring % data)
                except Exception, msg:
                    logger.warning('QSERVER: ERROR sending: %r', msg)
                else:
                    try:
                        data = self.readSocket(self.socket, socketTimeout=socketTimeout)
                        logger.debug('QSERVER: Received %r' % data)
                        return data
                    except Exception, msg:
                        logger.warning('QSERVER: ERROR reading: %r', msg)

            else:
                logger.debug('QSERVER: no writeable socket')

            time.sleep(0.05)

            retries += 1

            if retries >= maxRetries:
                logger.error('QSERVER: too much tries. Abording (%r)', data.strip())
                break

            logger.debug('QSERVER: retry sending %r (%s/%s)...', data.strip(), retries, maxRetries)

        logger.debug('QSERVER: Did not send any data')
        return 'QSERVER: Did not send any data'

    def sendRcon(self, data, maxRetries=None, socketTimeout=None):
        if socketTimeout is None:
            socketTimeout = self.socket_timeout
        if maxRetries is None:
            maxRetries = 2

        data = data.strip()
        # encode the data
        if self.encoding:
            data = self.encode_data(data, 'RCON')

        logger.debug('RCON sending (%s:%s) %r', self.host[0], self.host[1], data)
        startTime = time.time()

        retries = 0
        while time.time() - startTime < 5:
            readables, writeables, errors = select.select([], [self.socket], [self.socket], socketTimeout)

            if len(errors) > 0:
                logger.warning('RCON: %s', str(errors))
            elif len(writeables) > 0:
                try:
                    writeables[0].send(self.rconsendstring % (self.password, data))
                except Exception, msg:
                    logger.warning('RCON: ERROR sending: %r', msg)
                else:
                    try:
                        data = self.readSocket(self.socket, socketTimeout=socketTimeout)
                        logger.debug('RCON: Received %r' % data)
                        return data
                    except Exception, msg:
                        logger.warning('RCON: ERROR reading: %r', msg)

                if re.match(r'^quit|map(_rotate)?.*', data):
                    # do not retry quits and map changes since they prevent the server from responding
                    logger.debug('RCON: no retry for %r', data)
                    return 'RCON: Unknown response.'

            else:
                logger.debug('RCON: no writeable socket')

            time.sleep(0.05)

            retries += 1

            if retries >= maxRetries:
                logger.error('RCON: too much tries. Abording (%r)', data.strip())
                break
            logger.debug('RCON: retry sending %r (%s/%s)...', data.strip(), retries, maxRetries)

        logger.debug('RCON: Did not send any data')
        return 'RCON: Did not send any data'

    def stop(self):
        """Stop the rcon writelines queue"""
        self._stopEvent.set()

    def _writelines(self):
        while not self._stopEvent.isSet():
            lines = self.queue.get(True)

            self.lock.acquire()
            try:
                data = ''

                i = 0
                for cmd in lines:
                    if i > 0:
                        # pause and give time for last send to finish
                        time.sleep(1)

                    if not cmd:
                        continue

                    d = self.sendRcon(cmd)
                    if d:
                        data += d

                    i += 1
            finally:
                self.lock.release()

    def writelines(self, lines):
        self.queue.put(lines)

    def write(self, cmd, maxRetries=None, socketTimeout=None, Cached=True):
        #intercept status request for caching construct
        self.lock.acquire()
        try:
            data = self.sendRcon(cmd, maxRetries=maxRetries, socketTimeout=socketTimeout)
        finally:
            self.lock.release()

        if data:
            return data
        else:
            return ''

    def flush(self):
        pass

    def readNonBlocking(self, sock):
        sock.settimeout(2)

        startTime = time.time()

        data = ''
        while time.time() - startTime < 1:
            try:
                d = str(sock.recv(4096))
            except socket.error, detail:
                logger.debug('RCON: ERROR reading: %s' % detail)
                break
            else:
                if d:
                    # remove rcon header
                    data += d.replace(self.rconreplystring, '')
                elif len(data) > 0 and ord(data[-1:]) == 10:
                    break

        return data.strip()

    def readSocket(self, sock, size=4096, socketTimeout=None):
        if socketTimeout is None:
            socketTimeout = self.socket_timeout

        data = ''

        readables, writeables, errors = select.select([sock], [], [sock], socketTimeout)

        if not len(readables):
            raise Exception('No readable socket')

        while len(readables):
            d = str(sock.recv(size))

            if d:
                # remove rcon header
                data += d.replace(self.rconreplystring, '')

            readables, writeables, errors = select.select([sock], [], [sock], socketTimeout)

            if len(readables):
                logger.debug('RCON: More data to read in socket')

        return data.strip()

    def close(self):
        pass

    def getRules(self):
        self.lock.acquire()
        try:
            data = self.send('getstatus')
        finally:
            self.lock.release()

        if data:
            return data
        else:
            return ''

    def getInfo(self):
        self.lock.acquire()
        try:
            data = self.send('getinfo')
        finally:
            self.lock.release()

        if data:
            return data
        else:
            return ''
