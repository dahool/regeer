import os
from os import listdir, remove, rmdir
from os.path import isdir, islink
from ftplib import FTP
import re, tempfile
import urllib2

DIR_EXCLUDES = ('.', '..')

def deltree(topdir):
    """
    force to delete whole directory tree.
    """
    try:
        dirs = listdir(topdir)
    except OSError:
        return
    
    for dir in dirs:
        if dir in DIR_EXCLUDES:
            continue
        fpath = os.path.join(topdir, dir)
        if islink(fpath) or not isdir(fpath):
            try:
                if not os.access(fpath, os.W_OK):
                    os.chmod(fpath, 0777)
                remove(fpath)
            except OSError:
                pass
        else:
            deltree(fpath)
    try:
        rmdir(topdir)
    except OSError:
        pass

def getfile(name):
    if name.startswith("ftp://"):
        return getftpfile(name)
    if name.startswith("http://"):
        return gethttpfile(name)
    return open(name, 'rb')

def gethttpfile(url):
    try:
        resp = urllib2.urlopen(url)
        file = tempfile.TemporaryFile()
        file.write(resp.read())
        file.flush()
        file.seek(0)
        return file
    except Exception:
        raise

def getftpfile(url):
    import re, tempfile
    
    patterns = ['^ftp://(?P<user>[\w]+):(?P<password>[\w]+)@(?P<host>[\w\-\.]+):(?P<port>[\d]+)/(?P<path>.+)$',
                '^ftp://(?P<user>[\w]+):(?P<password>[\w]+)@(?P<host>[\w\-\.]+)/(?P<path>.+)$',
                '^ftp://(?P<host>[\w\-\.]+):(?P<port>[\d]+)/(?P<path>.+)$',
                '^ftp://(?P<host>[\w\-\.]+)/(?P<path>.+)$']
    for expr in patterns:
        m = re.match(expr, url, re.IGNORECASE)
        if m:
            d = m.groupdict()
            host = d.get('host')
            path = d.get('path')
            user = d.get('user')
            passwd = d.get('password')
            port = d.get('port')
            break
    if m:
        try:
            if port and port != 21:
                ftp = FTP()
                ftp.connect(host, int(port))
                if user:
                    ftp.login(user, passwd)
                else:
                    ftp.login()
            else:
                ftp = FTP(host, user, passwd)
            file = tempfile.TemporaryFile(suffix=os.path.basename(path))
            ftp.cwd(os.path.dirname(path))
            ftp.retrbinary('RETR ' + os.path.basename(path), file.write)
            file.flush()
            file.seek(0)
            ftp.close()
            return file
        except Exception, e:
            raise Exception("FTP: %s" % str(e))

FTP_FILE = 1
FTP_DIRECTORY = 2

class FtpFile:

    win_list_pat = re.compile('(\d{2}-\d{2}-\d{2})')
    
    def __init__(self, data, path=None):
        if self.win_list_pat.match(data):
            self._parse_win(data)
        else:
            self._parse_nix(data)
        self.path = path
            
    def _parse_nix(self, data):
        if data[0:1] == 'd':
            self.type = FTP_DIRECTORY
            self.size = 0
        else:
            self.type = FTP_FILE
            self.size = long(data[41:40])
        self.name = data[54:].strip()
    
    def _parse_win(self, data):
        if data[25:28] == 'DIR':
            self.type = FTP_DIRECTORY
            self.size = 0
        else:
            self.type = FTP_FILE
            self.size = long(data[29:38])
        self.name = data[39:].strip()
        
    @property
    def is_file(self):
        return self.type == FTP_FILE

    @property
    def is_directory(self):
        return self.type == FTP_DIRECTORY
        
class FtpClient:
    
    patterns = [re.compile('^ftp://(?P<user>[\w]+):(?P<password>[\w]+)@(?P<host>[\w\-\.]+):(?P<port>[\d]+)/(?P<path>.+)$', re.IGNORECASE),
                re.compile('^ftp://(?P<user>[\w]+):(?P<password>[\w]+)@(?P<host>[\w\-\.]+)/(?P<path>.+)$', re.IGNORECASE),
                re.compile('^ftp://(?P<host>[\w\-\.]+):(?P<port>[\d]+)/(?P<path>.+)$', re.IGNORECASE),
                re.compile('^ftp://(?P<host>[\w\-\.]+)/(?P<path>.+)$', re.IGNORECASE)]
    
    def __init__(self, connectionString):
        m = self._find_match(connectionString)
        if m:
            d = m.groupdict()
            self._host = d.get('host')
            self._user = d.get('user')
            self._passwd = d.get('password')
            self._port = d.get('port')
        else:
            raise Exception("Invalid connection string")

    def _find_match(self, connectionString):
        for expr in self.patterns:
            m = expr.match(connectionString)
            if m: break
        return m
            
    def _extract_path(self, url):
        if not url.startswith("ftp://"):
            return url
        m = self._find_match(url)
        if m:
            d = m.groupdict()
            return d.get('path')
        raise Exception("Invalid path. Appears to be an ftp connection string, but no path was found.")
        
    def _get_connection(self):
        if self._port and int(self._port)!= 21:
            ftp = FTP()
            ftp.connect(self._host, int(self._port))
            if self._user:
                ftp.login(self._user, self._passwd)
            else:
                ftp.login()
        else:
            ftp = FTP(self._host, self._user, self._passwd)
        return ftp
    
    def list_files(self, path):
        try:
            path = self._extract_path(path)
            ftp = self._get_connection()
            ftp.cwd(os.path.dirname(path))
            files = []
            ftp.retrlines('LIST',lambda line: files.append(FtpFile(line, os.path.dirname(path))))
            ftp.quit()
            return files
        except Exception, e:
            raise Exception("FTP: %s" % str(e))
        
    def get_file(self, path):
        try:
            path = self._extract_path(path)
            ftp = self._get_connection()
            tmpfile = tempfile.TemporaryFile(suffix=os.path.basename(path))
            ftp.cwd(os.path.dirname(path))
            ftp.retrbinary('RETR ' + os.path.basename(path), tmpfile.write)
            tmpfile.flush()
            tmpfile.seek(0)
            ftp.quit()
            return tmpfile
        except Exception, e:
            raise Exception("FTP: %s" % str(e))