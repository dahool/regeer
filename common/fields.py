from django.db import models
from django.db.models import fields
from common.crypto import BCipher
from common.utils.slug import slugify
from django.conf import settings

class CryptField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('max_length'):
            kwargs['max_length'] = 100
        super(CryptField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        cleartext = getattr(model_instance, self.attname)
        key = getattr(settings, 'SECRET_KEY')
        bc = BCipher(key)
        enc = bc.encrypt(cleartext)
        setattr(model_instance, self.attname, enc)
        return enc
    
    def to_python(self, value):
        value = super(CryptField, self).to_python(value)
        if value is not None:
            key = getattr(settings, 'SECRET_KEY')
            bc = BCipher(key)
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