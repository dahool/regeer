from django.utils.translation import ungettext_lazy as _
import re

def minutes2int(mins):
    if re.match('^[0-9.]+$', mins):
        return round(float(mins), 2)
    else:
        return 0
    
def time2minutes(timeStr):
    if not timeStr:
        return 0
    elif type(timeStr) is int:
        return timeStr

    timeStr = str(timeStr)
    if not timeStr:
        return 0
    elif timeStr[-1:] == 'h':
        return minutes2int(timeStr[:-1]) * 60
    elif timeStr[-1:] == 'm':
        return minutes2int(timeStr[:-1])
    elif timeStr[-1:] == 's':
        return minutes2int(timeStr[:-1]) / 60
    elif timeStr[-1:] == 'd':
        return minutes2int(timeStr[:-1]) * 60 * 24
    elif timeStr[-1:] == 'w':
        return minutes2int(timeStr[:-1]) * 60 * 24 * 7
    elif timeStr[-1:] == 'M':
        return minutes2int(timeStr[:-1]) * 60 * 24 * 31    
    else:
        return minutes2int(timeStr) 
    
def duration_human(seconds):
    seconds = long(round(seconds))
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    months, days = divmod(days, 30.4368499)
    #years, days = divmod(days, 365.242199)
    years, months = divmod(months, 12)
 
    minutes = long(minutes)
    hours = long(hours)
    days = long(days)
    months = long(months)
    years = long(years)
 
    duration = []
    if years > 0:
        duration.append(_('%d year', '%d years', years) % years)
    if months > 0:
        duration.append(_('%d month', '%d months', months) % months)        
    if days > 0:
        duration.append(_('%d day', '%d days', days) % days)
    if hours > 0:
        duration.append(_('%d hour', '%d hours', hours) % hours)
    if minutes > 0:
        duration.append(_('%d minute', '%d minutes', minutes) % minutes)
    if seconds > 0:
        duration.append(_('%d second', '%d seconds', seconds) % seconds)
    return ', '.join(duration)