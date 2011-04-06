import os, errno
import tempfile
import time
from app.log import (logger)

class LockException(Exception):
    pass
 
class Lock(object):
    """ This use mkdir to do the locking, as it is atomic
    """
    is_locked = False
  
    def __init__(self, name, timeout=5, delay=.05):
        self.lockpath = os.path.join(tempfile.gettempdir(), "%s.lock" % name)
        self.name = name
        self.timeout = timeout
        self.delay = delay
 
    def acquire(self):
        """ Acquire the lock, if possible. If the lock is in use, it check again
            every `wait` seconds. It does this until it either gets the lock or
            exceeds `timeout` number of seconds, in which case it throws 
            an exception.
        """
        start_time = time.time()
        while True:
            try:
                os.makedirs(self.lockpath,0777)
                break
            except OSError, e:
                logger.warn(e)
                if e.errno != errno.EEXIST:
                    logger.error(e)
                    raise 
                if (time.time() - start_time) >= self.timeout:
                    logger.error(e)
                    raise LockException("Timeout occured.")
                time.sleep(self.delay)
        self.is_locked = True
 
    def release(self):
        """ Get rid of the lock by deleting the lock. 
            When working in a `with` statement, this gets automatically 
            called at the end.
        """
        if self.is_locked:
            os.rmdir(self.lockpath)
            self.is_locked = False

 
    def __enter__(self):
        """ Activated when used in the with statement. 
            Should automatically acquire a lock to be used in the with block.
        """
        if not self.is_locked:
            self.acquire()
        return self
 
 
    def __exit__(self, type, value, traceback):
        """ Activated at the end of the with statement.
            It automatically releases the lock if it isn't locked.
        """
        if self.is_locked:
            self.release()
 
 
    def __del__(self):
        """ Make sure that the FileLock instance doesn't leave a lock
            lying around.
        """
        self.release()