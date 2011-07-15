from django.db import models
from b3connect.models import Client
from b3connect.fields import EpochDateTimeField
from b3portal.models import Server
from django.utils.translation import gettext_lazy as _

class FollowPlugin(models.Model):
    server = models.ForeignKey(Server, related_name="follow_plugin", unique=True, verbose_name=_('Server'))

    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return str(self.server)
    
    class Meta:
        verbose_name = _('Follow')
        verbose_name_plural = _('Follow')
        db_table = 'plugin_follow'   
            
class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client,
                               db_column="client_id",
                               to_field="id",
                               related_name="followed")
    admin = models.ForeignKey(Client, db_column="admin_id", to_field="id", related_name="following")
    reason = models.CharField(max_length=100, blank=True, null=True)
    time_add = EpochDateTimeField()
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s [%s]" % (self.client.name,self.time_add.strftime("%d/%m/%Y %H:%M"))
        
    class Meta:
        managed = False
        ordering = ('client',)
        verbose_name_plural = "Following"
        db_table = u'following'
        permissions = (
            ("view_follow", "View follow info"),
        )