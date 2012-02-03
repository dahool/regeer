from django.core.files.storage import FileSystemStorage
from django.core.files import File
from common.utils.file import getftpfile, gethttpfile
from django.core.files.base import ContentFile
import re, os, time

def url_to_string(url):
    return re.sub("[\:/\.\?\&\ @]","_", url)

class RemoteCachedFileSystemStorage(FileSystemStorage):
    
    def __init__(self, location=None, base_url=None, cache_time=None):
        super(RemoteCachedFileSystemStorage, self).__init__(location, base_url)
        if cache_time:
            self._cache_time = cache_time * 60
        else:
            self._cache_time = 300
            
    def _is_cached(self, name):
        if os.path.exists(self.path(name)):
            mtime = os.path.getmtime(name)
            if mtime + self._cache_time > time.time():
                return True
        return False
            
    def _savelocal(self, fileobj, name):
        file_content = ContentFile(fileobj.read())
        self._save(name, file_content)

    def _save(self, name, content):
        full_path = self.path(name)
        if os.path.exists(full_path):
            os.remove(full_path)
        super(RemoteCachedFileSystemStorage, self)._save(name, content)
        
    def _open(self, name, mode='rb'):
        if name.startswith("ftp://") or name.startswith("http://"):
            localfilename = url_to_string(name)
            localname = self.path(localfilename)
            if not self._is_cached(localname):
                fobj = gethttpfile(name)
                self._savelocal(fobj, localfilename)
        else:
            localname = name
        return File(open(localname, mode))