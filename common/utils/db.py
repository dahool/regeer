from django.db.utils import DEFAULT_DB_ALIAS
from django.db import connections

def db_table_exists(table, cursor=None, using=DEFAULT_DB_ALIAS):
    try:
        connection = None
        connection = connections[using]
        if not cursor:
            cursor = connections[using].cursor()
        if not cursor:
            raise Exception
        table_names = connection.introspection.get_table_list(cursor)
    except:
        raise Exception("unable to determine if the table '%s' exists" % table)
    else:
        return table in table_names