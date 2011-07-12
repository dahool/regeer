from django.db import models
from b3connect.models import Client
from b3connect.fields import EpochDateTimeField

class NickReg(models.Model):
    nickid = models.IntegerField(db_index=True)
    name = models.CharField(unique=True, max_length=32)
    client = models.ForeignKey(Client, db_column="clientid", related_name="nicks", to_field="id")
    time_add = EpochDateTimeField()
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s [%s]" % (self.client.name,self.name)
        
    class Meta:
        managed = False
        ordering = ('client',)
        verbose_name_plural = "Nicks"
        db_table = u'nicks'