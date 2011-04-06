from django.db.models.signals import post_save, pre_delete

class LoggingModel(object):
    
    def register(self, model):
        post_save.connect(self.log_addition, sender=model)
        pre_delete.connect(self.log_deletion, sender=model)
    
    def log_addition(self, sender, **kwargs):
        """
        Log that an object has been successfully added.
        """
        from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
        from django.contrib.contenttypes.models import ContentType
        from django.utils.encoding import force_unicode
        
        object = kwargs.get('instance')
        created = kwargs.get('created')
        
        LogEntry.objects.log_action(
            user_id         = 1,#request.user.pk,
            content_type_id = ContentType.objects.get_for_model(object).pk,
            object_id       = object.pk,
            object_repr     = force_unicode(object),
            action_flag     = ADDITION if created else CHANGE
        )
    
    def log_deletion(self, sender, **kwargs):
        """
        Log that an object has been successfully deleted. Note that since the
        object is deleted, it might no longer be safe to call *any* methods
        on the object, hence this method getting object_repr.
        """
        from django.contrib.admin.models import LogEntry, DELETION
        from django.contrib.contenttypes.models import ContentType
        from django.utils.encoding import force_unicode
            
        object = kwargs.get('instance')
        
        LogEntry.objects.log_action(
            user_id         = 1, #request.user.id,
            content_type_id = ContentType.objects.get_for_model(object).pk,
            object_id       = object.pk,
            object_repr     = force_unicode(object),
            action_flag     = DELETION
        )
    
site = LoggingModel()