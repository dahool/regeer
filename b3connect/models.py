import hashlib as hash
import time, datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.utils.functions import duration_human
from django.db.models import Q

from b3connect.fields import EpochDateTimeField

class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=96)
    keyword = models.CharField(unique=True, max_length=96, blank=True)
    level = models.IntegerField(blank=True, default=0)
    time_edit = EpochDateTimeField()
    time_add = EpochDateTimeField()

    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s (Level %d)" % (self.name, self.level)
    
    class Meta:
        ordering  = ('id',)
        db_table = u'groups'
        permissions = (
            ("view_group", "Can view groups"),
        )
                
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=48)
    connections = models.IntegerField()
    guid = models.CharField(unique=True, max_length=96)
    pbid = models.CharField(max_length=96, blank=True)
    name = models.CharField(max_length=96)
    auto_login = models.IntegerField()
    mask_level = models.IntegerField()
    group = models.ForeignKey(Group, to_field="id", db_column="group_bits", default=0, null=True, blank=True)
    greeting = models.CharField(max_length=384, blank=True)
    login = models.CharField(max_length=48, blank=True)
    password = models.CharField(max_length=96, blank=True)
    time_edit = EpochDateTimeField()
    time_add = EpochDateTimeField()

    def __unicode__(self):
        return repr(self)
    
    def __repr__(self):
        if self.group_id > 0:
            return "%s - %s (%s)" % (self.id, self.name, self.group.name)
        else:
            return "%s - %s" % (self.id, self.name)
        
    @property
    def displayGroup(self):
        if self.group_id > 0:
            return self.group
        else:
            return _('Un-registered')
        
    @property
    def masked_ip(self):
        ips = self.ip.split(".")
        return ".".join(ips[:-1]) + ".XXX"
    
    def check_password(self, password):
        if self.password == '':
            return False
        return self.password == hash.md5(password).hexdigest()
        
    class Meta:
        ordering = ('id',)
        db_table = u'clients'
        permissions = (
            ("view_client", "Can view clients"),
            ("change_client_group", "Can change client group"),
            ("register_client", "Can register client"),
            ("view_high_level_client", "Can view high level clients"),
            ("client_advanced_search", "Can run advanced search"),
        )

class Alias(models.Model):
    id = models.AutoField(primary_key=True)
    num_used = models.IntegerField()
    ip = models.CharField(max_length=16, blank=True, null=True)
    alias = models.CharField(unique=True, max_length=96)
    client = models.ForeignKey(Client, db_column="client_id", related_name="aliases", to_field="id")
    time_edit = EpochDateTimeField()
    time_add = EpochDateTimeField()
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s [%s] - [%s]" % (self.client.name,self.alias, self.ip)
        
    class Meta:
        ordering = ('-time_edit',)
        verbose_name_plural = "Aliases"
        db_table = u'aliases'
        permissions = (
            ("view_aliases", "Can view aliases"),
        )
        
PENALTY_CHOICES = (
    ('Warning', _('Warning')),
    ('Notice', _('Notice')),
    ('Ban', _('Ban')),
    ('TempBan', _('TempBan')),
    ('Kick', _('Kick')),
)

class PenaltyManager(models.Manager):
    
    def active(self):
        return self.filter(Q(time_expire='-1') | Q(time_expire__gt=int(time.time())),inactive=0)

    def active_bans(self):
        return self.filter(Q(time_expire='-1') | Q(time_expire__gt=int(time.time())),
                    (Q(type='Ban') | Q(type='TempBan')),inactive=0)

    def notices(self):
        return self.filter(type='Notice',inactive=0)
        
    def inactive(self):
        return self.filter(Q(inactive=1) | Q(time_expire__lt=int(time.time()))).exclude(
                                    Q(inactive=0) & Q(time_expire='-1')                                                                                        
                                                                                        )
        
    def noexpired(self):
        return self.filter(Q(time_expire='-1') | Q(time_expire__gt=int(time.time())))
    
class Penalty(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=21, choices=PENALTY_CHOICES)
    client = models.ForeignKey(Client, db_column="client_id", related_name="penalties", to_field="id")
    admin = models.ForeignKey(Client, db_column="admin_id", to_field="id", blank=True, default=0, null=True, related_name="adminpenalties")
    duration = models.IntegerField()
    inactive = models.IntegerField(default=0)
    keyword = models.CharField(max_length=48, blank=True,default='')
    reason = models.CharField(max_length=765)
    data = models.CharField(max_length=765, blank=True, default='')
    time_edit = EpochDateTimeField()
    time_add = EpochDateTimeField()
    time_expire = EpochDateTimeField(blank=True)

    objects = PenaltyManager()
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s - %s [%s] (%s)" % (self.client.name,
                                      self.type,
                                      self.reason,
                                      self.time_add.strftime("%d/%m/%Y %H:%M"))
    
    class Meta:
        ordering = ('-time_add',)
        verbose_name_plural = "Penalties"
        db_table = u'penalties'
        permissions = (
            ("view_penalty", "Can view penalties"),
            ("view_notices", "Can view notices"),
            ("view_banlist", "Can view ban list"),
            ("add_notice", "Add notice"),
        )
        
    @property
    def display_duration(self):
        if self.duration > 0:
            return duration_human(self.duration*60)
        return ''
    
    @property
    def is_expired(self):
        return self.time_expire < datetime.datetime.now()
        
    def save(self, force_insert=False, force_update=False):
        if self.duration == 0 and self.type == 'Ban':
            self.time_expire = -1
        else:
            self.time_expire =  int(time.mktime(self.time_add.timetuple())) + (self.duration * 60)
        super(Penalty, self).save(force_insert, force_update)
        
class Nick(models.Model):
    nickid = models.IntegerField(db_index=True)
    name = models.CharField(unique=True, max_length=32)
    client = models.ForeignKey(Client, db_column="clientid", related_name="nicks", to_field="id")
    time_add = EpochDateTimeField()
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s [%s]" % (self.client.name,self.name)
        
    class Meta:
        ordering = ('client',)
        verbose_name_plural = "Nicks"
        db_table = u'nicks'
        
class DisabledCommand(models.Model):
    id = models.AutoField(primary_key=True)
    cmd = models.CharField(unique=True, max_length=50)
    until = EpochDateTimeField()
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s [%s]" % (self.cmd,self.until)
        
    class Meta:
        db_table = u'disabledcmd'
        
class AuditLog(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, db_column="client_id", to_field="id", related_name="commands")
    command = models.CharField(max_length=20, db_index=True)
    data = models.CharField(max_length=50, blank=True, null=True)
    time_add = EpochDateTimeField(db_index=True)
    
    def __unicode__(self):
        return repr(self)
    
    def __repr__(self):
        return "%s: %s" % (self.client.name, self.command)
    
    class Meta:
        ordering = ('-time_add',)
        db_table = u"auditlog"