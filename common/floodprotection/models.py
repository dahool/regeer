from django.db import models
from django.contrib.auth.models import Group

class GroupFloodSettings(models.Model):
    group = models.ForeignKey(Group, related_name='floodsettings', unique=True)
    timeout = models.IntegerField(default=30)
    
    def __unicode__(self):
        return "%s - %s" % (self.group, self.timeout)