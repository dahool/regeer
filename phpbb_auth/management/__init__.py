from django.db.models import signals
from django.contrib.auth import models as auth_app

def initialize_db(app, created_models, verbosity, **kwargs):
    from django.core.management import call_command
    call_command("initdb")
        
signals.post_syncdb.connect(initialize_db,
    sender=auth_app, dispatch_uid = "b3portal.management.initdb")