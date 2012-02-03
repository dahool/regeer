from django.db import models
from django.db.models import fields
from django.db.models.fields import files
from common.crypto import BCipher
from common.utils.slug import slugify
from djangocommonutils.file.storage import RemoteCachedFileSystemStorage
from django.conf import settings
import os

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
    
class RemoteCachedFileField(files.FileField):
    
    def __init__(self, verbose_name=None, name=None, upload_to='', cache_time=None, **kwargs):
        storage = RemoteCachedFileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, upload_to),
                                                    cache_time=cache_time)
        super(RemoteCachedFileField, self).__init__(verbose_name, name, upload_to, storage, **kwargs) 
    