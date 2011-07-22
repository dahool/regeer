# -*- coding: utf-8 -*-
"""Copyright (c) 2010 Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
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