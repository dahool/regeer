import urllib2
import xml.etree.ElementTree as ET
from djangogravatar import settings
from djangogravatar.util import email_hash
    
class ProfileNotFound(Exception):
    pass

class UserProfile(object):
    
    def __init__(self, email, prefetch = True):
        self.email = email
        if prefetch:
            self.fetch()

    def _get_field(self, path):
        try:
            return self.entry.find(path).text
        except:
            return None
        
    def fetch(self):
        url = settings.GRAVATAR_URL + email_hash(self.email) + ".xml" 
        try:
            result = urllib2.urlopen(url)
        #except urllib2.URLError, e:
        except Exception, e:
            raise ProfileNotFound(e)
 
        tree = ET.parse(result)
        self.entry = tree.getroot().find('entry')
        self.preferredUsername = self._get_field('entry/preferredUsername')
        self.profileUrl = self._get_field('entry/profileUrl')
        self.thumbnailUrl = self._get_field('entry/thumbnailUrl')
        self.displayName = self._get_field('entry/displayName')
        self.aboutMe = self._get_field('entry/aboutMe')
        self.currentLocation = self._get_field('entry/currentLocation')
        self.photos = []
        for photo in self.entry.findall('photos'):
            try:
                self.photos.append(photo.find('value').text)
            except:
                pass
        self.emails = []
        for m in self.entry.findall('emails'):
            try:
                self.emails.append(m.find('value').text)
            except:
                pass