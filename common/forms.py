from django.forms.util import ErrorList
from django.utils.safestring import mark_safe

class TipErrorList(ErrorList):
    
    def __unicode__(self):
        return self.as_tips()
    
    def as_tips(self):
        if not self: return u''
        return u'<span class="field-error" title="%s"></span>' % ','.join(e for e in self)
        