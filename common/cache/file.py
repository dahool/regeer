import os
import tempfile
import time
import base64
import pickle
import logging

logger = logging.getLogger('regeer')

class FileCache:
    
    def __init__(self, name, expireInMinutes = 1, prefix = 'tmp', suffix = 'cache'):
        self.expire = expireInMinutes * 60
        self.name = os.path.join(tempfile.gettempdir(), prefix + name + "." + suffix)
         
    def load(self):
        data = None
        if os.path.exists(self.name):
            mtime = os.path.getmtime(self.name)
            if mtime + self.expire > time.time():
                _file = None
                try:
                    _file = open(self.name,'rb')
                    data = pickle.loads(base64.b64decode(_file.read()))
                except:
                    logger.exception('load %s' % self.name)
                finally:
                    if _file: _file.close()
            else:
                try:
                    # lets clean up if expired
                    os.unlink(self.name)
                except:
                    pass
        return data

    def save(self, data):
        _file = None
        try:
            _file = open(self.name, 'wb')
            _file.write(base64.b64encode(pickle.dumps(data)))
            _file.flush()
        except:
            logger.exception('save %s' % self.name)
        finally:
            if _file: _file.close()            