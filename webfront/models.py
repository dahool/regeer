from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from common.fields import CryptField, AutoSlugField

import re
from common.crypto import BCipher

DISPLAY_SUB = re.compile(r'ut4_|ut_|ut42_')

class Map(models.Model):
    name = models.CharField(max_length=50)
    server = models.CharField(max_length=50)
    
    @property
    def display_name(self):
        return DISPLAY_SUB.sub('',self.name).strip().title() 
    
    @property
    def map_image(self):
        return settings.MAP_IMAGE_URL % self.name
    
    @property
    def map_link(self):
        if not self.name in settings.SKIP_MAPS:
            return settings.MAP_LOCATION % self.name
        return None
    
    @property
    def server_name(self):
        return settings.SERVERS[self.server]['TITLE']
        
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering  = ('server','name')
        
        
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    canChangePassword = models.BooleanField(_('Can Change Password'), default=True,
                                            help_text=_('Allow the user to change login password'))

    def __repr__(self):
        return self.user.username
    
    def __unicode__(self):
        return repr(self)
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
    
DB_ENGINES_CHOICES = (
    ('django.db.backends.mysql', 'mysql'),
    ('django.db.backends.postgresql', 'postgresql'),
    ('django.db.backends.postgresql_psycopg2','postgresql_psycopg2'),
    ('django.db.backends.sqlite3','sqlite3'),
    ('django.db.backends.oracle','oracle')
)
    
class Server(models.Model):
    slug = AutoSlugField(max_length=50, unique=True, editable=False,prepopulate_from="name", force_update=False)
    name = models.CharField(max_length=40, verbose_name=_('Server Name'))
    database = models.CharField(max_length=50, verbose_name=_('Database Name'))
    engine = models.CharField(max_length=100, choices=DB_ENGINES_CHOICES, verbose_name=_('Database Engine'))
    user = models.CharField(max_length=50, verbose_name=_('Database User'))
    password = models.CharField(max_length=200)
    hostname = models.CharField(max_length=50, verbose_name=_('Database Host'))
    status_file = models.CharField(max_length=255, verbose_name=_('Status File Abs Path'), help_text=_('For status plugin'), blank=True)
    config_file = models.CharField(max_length=255, verbose_name=_('Config File Abs Path'), help_text=_('For RCON access'), blank=True)
    
    def __repr__(self):
        return self.name
    
    def set_password(self, clear_text):
        bc = BCipher()
        setattr(self, 'password', bc.encrypt(clear_text))

    def get_password(self):
        value = getattr(self, 'password', None)
        if value is not None:
            bc = BCipher()
            return bc.decrypt(value)
        return value

    class Meta:
        ordering  = ('name',)
        unique_together = ('database','user','hostname')
                
class Plugins(models.Model):
    server = models.ForeignKey(Server, related_name="plugins")
    name = models.CharField(max_length=20)
    
    def __repr__(self):
        return "%s [%s]" % (self.name,repr(self.server))