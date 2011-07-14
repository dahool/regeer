from django.db import models
from django.utils.translation import ugettext_lazy as _
from b3connect.models import Client
from b3connect.fields import EpochDateTimeField
from b3portal.models import Server

CHAT_TARGETS = {'ALL': _('Everyone'),
                'TEAM: BLUE': _('Blue Team'),
                'TEAM: RED': _('Red Team')}

class ChatLogPlugin(models.Model):
    server = models.ForeignKey(Server, related_name="chatlog_plugin", unique=True, verbose_name=_('Server'))

    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return str(self.server)

class ChatLog(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, db_column="client_id", to_field="id", related_name="chats")
    data = models.CharField(max_length=100, blank=True, null=True)
    info = models.CharField(max_length=255, blank=True, null=True)
    target = models.CharField(max_length=50, blank=True, null=True)
    time_add = EpochDateTimeField(db_index=True)
    
    def __unicode__(self):
        return repr(self)
    
    def __repr__(self):
        return "%s: %s" % (self.client.name, self.data)
    
    @property
    def target_display(self):
        return CHAT_TARGETS.get(self.target,self.target)
    
    class Meta:
        managed = False
        ordering = ('-time_add',)
        db_table = u"chatlog"
        permissions = (
            ("view_chat", "Can view chat logs"),
        )