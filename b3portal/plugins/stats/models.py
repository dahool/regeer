from django.db import models
from b3connect.models import Client
from b3connect.fields import EpochDateTimeField

class KnifeStat(models.Model):
    map_name = models.CharField(max_length=255, primary_key=True)
    client = models.ForeignKey(Client, db_column='playerid')
    score = models.IntegerField(blank=True, default=0)
    time_add = EpochDateTimeField()

    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s - %s" % (self.client.name, self.map_name)
    
    class Meta:
        managed = False
        db_table = u'plugin_knife_hof'

class NaderStat(models.Model):
    map_name = models.CharField(max_length=255, primary_key=True)
    client = models.ForeignKey(Client, db_column='playerid')
    score = models.IntegerField(blank=True, default=0)
    time_add = EpochDateTimeField()

    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return "%s - %s" % (self.client.name, self.map_name)
    
    class Meta:
        managed = False
        db_table = u'plugin_nader_hef'
        
class FlagStat(models.Model):
    mapname = models.CharField(max_length=255, primary_key=True)
    most_capture_client = models.ForeignKey(Client, db_column='most_capture_client', related_name="captured_flags")
    most_capture_score = models.IntegerField(default=0)
    most_capture_timeadd = EpochDateTimeField()
    quick_capture_client = models.ForeignKey(Client, db_column='quick_capture_client', related_name="quickest_captured_flags")
    quick_capture_score = models.FloatField(default=999.0)
    quick_capture_timeadd = EpochDateTimeField()
    
    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return self.mapname
    
    class Meta:
        managed = False
        db_table = u'flagstats'        