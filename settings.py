# Django settings for pureftpman project.
import os
import glob

PROJECT_PATH = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))

conffiles = glob.glob(os.path.join(os.path.dirname(__file__), 'settings','*.pyconf'))
conffiles.sort()

for f in conffiles:
    execfile(os.path.abspath(f)) 
    
if os.path.exists(LOCAL_CONFIG):
    execfile(LOCAL_CONFIG)