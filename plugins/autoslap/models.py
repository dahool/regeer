from django.db import models
from b3connect.models import Client
from b3connect.fields import EpochDateTimeField

class AutoSlap(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client,
                               db_column="client_id",
                               to_field="id",
                               related_name="autoslaps")
    admin = models.ForeignKey(Client, db_column="admin_id", to_field="id")
    reason = models.CharField(max_length=100, blank=True, null=True)
    time_add = EpochDateTimeField()
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s [%s]" % (self.client.name,self.time_add.strftime("%d/%m/%Y %H:%M"))
        
    class Meta:
        managed = False
        ordering = ('client',)
        verbose_name_plural = "AutoSlaps"
        db_table = u'tb_autoslap'
        permissions = (
            ("view_autoslap", "Can view autoslaps"),
        )        