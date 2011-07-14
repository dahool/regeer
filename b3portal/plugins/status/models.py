from django.db import models
from b3connect.models import Client
from b3portal.models import Server
from django.utils.translation import gettext_lazy as _

class StatusPlugin(models.Model):
    server = models.ForeignKey(Server, related_name="status_plugin", unique=True, verbose_name=_('Server'))
    location = models.CharField(max_length=500, verbose_name=_('Status File Location'))

    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return str(self.server)
    
class ServerStatus(models.Model):
    server = models.ForeignKey(Server)
    map = models.CharField(max_length=100, db_index=True)
    time_add = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s - %s - %d" % (str(self.server), str(self.time_add), self.totalPlayers)
    
    @property
    def totalPlayers(self):
        return self.players.count()
    
    def is_online(self, client_id):
        for c in self.players.all():
            if c.client_id == client_id:
                return True
        return False
    
    class Meta:
        ordering = ('-time_add',)
        get_latest_by = ('time_add',)
        permissions = (
            ("view_serverstatus", "Can view Server Status"),
        )
        
class StatusClient(models.Model):
    status = models.ForeignKey(ServerStatus, related_name='players')
    client_id = models.IntegerField()
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s - %s" % (str(self.status), self.client_id)
    
    @property
    def client(self):
        return Client.objects.using(self.status.server.uuid).get(pk=self.client_id)