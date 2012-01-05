# Django settings for pureftpman project.
import os
import glob

LOCAL_CONFIG = None
VERSION = None

PROJECT_PATH = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))

conffiles = glob.glob(os.path.join(os.path.dirname(__file__), 'settings','*.pyconf'))
conffiles.sort()

for f in conffiles:
    execfile(os.path.abspath(f)) 

if LOCAL_CONFIG and os.path.exists(LOCAL_CONFIG):
    execfile(LOCAL_CONFIG)
    
try:
    # lets check if b3 is in the python path
    import b3
except:
    B3_INSTALLED = False
else:
    B3_INSTALLED = True
B3_INSTALLED = False    

if os.path.exists(os.path.join(PROJECT_PATH,'build.ver')):
    import time
    st = os.stat(os.path.join(PROJECT_PATH,'build.ver'))
    VERSION += " build %s" % time.strftime("%Y%m%dT%H%M",time.localtime(st.st_mtime))
