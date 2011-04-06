import os
from os import listdir, remove, rmdir
from os.path import isdir, islink

DIR_EXCLUDES = ('.', '..')

def deltree(topdir):
    """
    force to delete whole directory tree.
    """
    try:
        dirs = listdir(topdir)
    except OSError, why:
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
            except OSError, why:
                pass
        else:
            deltree(fpath)
    try:
        rmdir(topdir)
    except OSError, why:
        pass
