from django.conf import settings

PHPBB_DB = getattr(settings, 'PHPBB_DB_ID', 'phpbb')

class phpbbRouter(object):
    
    def _is_bb(self, model):
#            if model.__class__.__name__ in ('bbUser','bbGroup','bbAclRole','bbAclOption','bbUserGroup'): 
        if hasattr(model, '_meta'):       
            if model._meta.app_label == 'phpbb_auth':
                return True
        return False
    
    def db_for_read(self, model, **hints):
        if self._is_bb(model):
            return PHPBB_DB
        return None

    def db_for_write(self, model, **hints):
        if self._is_bb(model):
            return PHPBB_DB
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        return None
    
    def allow_syncdb(self, db, model):
        if self._is_bb(model):
            return False
        return None