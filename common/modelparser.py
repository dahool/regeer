import time
import datetime
import types
from decimal import *
from django.db import models

def parse(data, exclude = None, force = None):
    """Parse any model to python dict"""

    def _any(data):
        ret = None
        if type(data) is types.ListType:
            ret = _list(data)
        elif type(data) is types.DictType:
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            #ret = str(data)
            ret = float(data)
        elif isinstance(data, models.query.QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, models.Model):
            ret = _model(data)
        elif isinstance(data, datetime.date):
            #ret = time.strftime("%Y/%m/%d",data.timetuple())
            ret = str(data)
        elif ('%s.%s' % (data.__class__.__module__,data.__class__.__name__)) == 'django.db.models.fields.related.RelatedManager':
            ret = _list(data.all())
        else:
            ret = data
        return ret
    
    def _model(data):
        ret = {}
        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            if f.attname not in exclude:
                ret[f.attname] = _any(getattr(data, f.attname))
        # And additionally encode arbitrary properties that had been added.
        fields = dir(data.__class__) + ret.keys()
        add_ons = [k for k in dir(data) if k not in fields]
        for k in add_ons:
            if k not in exclude:
                ret[k] = _any(getattr(data, k))
        force_fields = [k for k in force if k not in ret.keys() and k not in exclude]
        for k in force_fields:
            if hasattr(data, k):
                ret[k] = _any(getattr(data, k))                
        return ret
    
    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret
    
    def _dict(data):
        ret = {}
        for k,v in data.items():
            if k not in exclude:
                ret[k] = _any(v)
        return ret
    
    if exclude is None:
        exclude = []
    if force is None:
        force = []
    ret = _any(data)
    
    return ret