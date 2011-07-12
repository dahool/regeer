
def init_database_config():
    from models import Server
    from django.conf import settings
    
    try:
        from django.db import connections
        for server in Server.objects.all():
            # we want to ensure some of the database settings
            # were update to avoid recreating an existing connection
            if settings.DATABASES.has_key(server.uuid):
                current = settings.DATABASES[server.uuid]
                if (current['NAME'] == server.database and
                     current['ENGINE'] == server.engine and
                     current['USER'] == server.user and
                     current['PASSWORD'] == server.password and
                     current['HOST'] == server.hostname):
                    continue
            settings.DATABASES[server.uuid] = {
                'NAME': server.database,
                'ENGINE': server.engine,
                'USER': server.user,
                'PASSWORD': server.password,
                'HOST': server.hostname,
            }
            # force to recreate the connection
            del connections._connections[server.uuid]
    except Exception, e:
        pass
