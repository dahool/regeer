from django.db import models
from django.utils.encoding import smart_unicode

class ExceptionLog(models.Model):
    
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    exception = models.TextField(null=True, blank=True)
    stacktrace = models.TextField(null=True, blank=True)
    request = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return '%s - %s' % (smart_unicode(self.date),smart_unicode(self.exception))
    
    def __repr__(self):
        return smart_unicode(self) 
    
    class Meta:
        ordering  = ('-date',)    