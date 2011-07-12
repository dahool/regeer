from django.db import models
from b3connect.fields import EpochDateTimeField
from b3portal.models import Server

class StatusPlugin(models.Model):
    server = models.ForeignKey(Server, related_name="status_plugin", unique=True)
    location = models.CharField(max_length=500)

    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return self.server
    
class ServerStatus(models.Model):
    server = models.ForeignKey(Server)
    map = models.CharField(max_length=255, db_index=True)
    totalPlayers = models.IntegerField(default=0)
    time_add = EpochDateTimeField()

    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s - %s - %d" % (self.server, str(self.time_add), self.totalPlayers)
    
    class Meta:
        ordering = ('-time_add',)
        permissions = (
            ("view_serverstatus", "Can view Server Status"),
        )
        
class ServerStatusPlayers(models.Model):
    server = models.ForeignKey(ServerStatus, related_name='players')
    clientid = models.IntegerField(db_index=True)