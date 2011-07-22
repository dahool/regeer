from django.db import models
from django.db.models import fields
from common.crypto import BCipher
from common.utils.slug import slugify

class CryptField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('max_length'):
            kwargs['max_length'] = 100
        super(CryptField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None and value != '':
            bc = BCipher()
            enc = bc.encrypt(value)
        else:
            enc = value
        return enc
    
    def to_python(self, value):
        value = super(CryptField, self).to_python(value)
        if value is not None and value != '':
            bc = BCipher()
            return bc.decrypt(value)
        return value

class AutoSlugField(fields.SlugField):
    def __init__(self, prepopulate_from = None, force_update = False, *args, **kwargs):
        self.prepopulate_from = prepopulate_from
        self.force_update = force_update
        super(AutoSlugField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if self.prepopulate_from:
            value = slugify(model_instance, self, getattr(model_instance, self.prepopulate_from), self.force_update)
        else:
            value = super(AutoSlugField, self).pre_save(model_instance, add)
        setattr(model_instance, self.attname, value)
        return value