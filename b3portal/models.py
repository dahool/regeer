from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from common.fields import CryptField, AutoSlugField

import re
from common.crypto import BCipher

DISPLAY_SUB = re.compile(r'ut4_|ut_|ut42_')

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

PARSER_CHOICES = [(v,v) for v in settings.B3_PARSERS]

class Server(models.Model):
    uuid = AutoSlugField(max_length=50, unique=True, editable=False,prepopulate_from="name", force_update=False)
    name = models.CharField(max_length=40, verbose_name=_('Server Name'))
    database = models.CharField(max_length=50, verbose_name=_('Database Name'))
    engine = models.CharField(max_length=100, choices=DB_ENGINES_CHOICES, verbose_name=_('Database Engine'))
    user = models.CharField(max_length=50, verbose_name=_('Database User'))
    password = models.CharField(max_length=200)
    hostname = models.CharField(max_length=50, verbose_name=_('Database Host'))
    rcon_ip = models.IPAddressField(verbose_name=_('IP'), blank=True)
    rcon_port = models.IntegerField(verbose_name=_('Port'), blank=True, null=True)
    rcon_password = models.CharField(max_length=50, verbose_name=_('RCON Password'), blank=True)
    parser = models.CharField(max_length=15, choices=PARSER_CHOICES, verbose_name=_('Game'), blank=True) 
    default = models.BooleanField(default=False, verbose_name=_('Default'), help_text=_('Set as default server'))
    
    def __repr__(self):
        return self.name
    
    def __unicode__(self):
        return repr(self)
        
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

class MapCycle(models.Model):
    server = models.ForeignKey(Server, related_name="mapcycle", unique=True)
    location = models.CharField(max_length=500)

    def __repr__(self):
        return str(self.server)
    
    def __unicode__(self):
        return repr(self)
    
class Map(models.Model):
    server = models.ForeignKey(Server, related_name="maps")
    name = models.CharField(max_length=50)
    
    @property
    def display_name(self):
        return DISPLAY_SUB.sub('',self.name).strip().title() 
    
    @property
    def map_image(self):
        return settings.MAP_IMAGE_URL % self.name
    
    @property
    def map_link(self):
        if not self.name in settings.SKIP_MAPS:
            if settings.MAP_LOCATION:
                return settings.MAP_LOCATION % self.name
        return None
        
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering  = ('server','name')
                        
class Plugins(models.Model):
    server = models.ForeignKey(Server, related_name="plugins")
    name = models.CharField(max_length=50)
    
    def __repr__(self):
        return "%s [%s]" % (self.name,repr(self.server))

    def __unicode__(self):
        return repr(self)
    
    class Meta:
        verbose_name_plural = "Plugins"
        
class PluginConf(models.Model):
    plugin = models.ForeignKey(Plugins, related_name="config")
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=500)
    
    def __repr__(self):
        return "%s [%s: %s]" % (str(self.plugin), self.name, self.value)

    def __unicode__(self):
        return repr(self)
        
from b3portal import init_database_config
init_database_config()

def update_db_callback(sender, **kwargs):
    init_database_config()

from django.db.models.signals import post_save
post_save.connect(update_db_callback, sender=Server)    