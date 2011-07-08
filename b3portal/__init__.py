
def init_database_config():
    from models import Server
    from django.conf import settings
    
    try:
        for server in Server.objects.all():
            settings.DATABASES[server.uuid] = {
                    'NAME': server.database,
                    'ENGINE': server.engine,
                    'USER': server.user,
                    'PASSWORD': server.password,
                    'HOST': server.hostname,
                }
    except Exception, e:
        print e
