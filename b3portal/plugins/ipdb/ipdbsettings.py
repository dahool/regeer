from django.conf import settings

IPDB_URL =  getattr(settings, 'IPDB_URL','http://api.iddb.com.ar/api/v4/xmlrpc')
IPDB_TIMEOUT = getattr(settings, 'IPDB_TIMEOUT', 15)