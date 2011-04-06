from django.template import Variable, Library
import datetime

register = Library()

def timesincesec(value, arg=None):
    """Formats a date as the time since that date with minimun value as seconds (i.e. "4 days, 6 hours")."""
    from common.utils.timesince import timesince
    if not value:
        return u''
    try:
        if arg:
            return timesince(value, arg)
        return timesince(value)
    except (ValueError, TypeError):
        return u''
timesincesec.is_safe = False
register.filter(timesincesec)

def summinutes(value, min):
    v = datetime.timedelta(minutes=min)
    return value + v
register.filter(summinutes)