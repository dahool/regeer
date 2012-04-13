import datetime

from django.utils.tzinfo import LocalTimezone
from django.utils.translation import ungettext, ugettext

def minutes_to_string(ts):

    chunks = (
#          (60 * 60 * 60 * 24 * 365, lambda n: ungettext('year', 'years', n)),
#          (60 * 60 * 60 * 24 * 30, lambda n: ungettext('month', 'months', n)),
#          (60 * 60 * 60 * 24 * 7, lambda n : ungettext('week', 'weeks', n)),
#          (60 * 60 * 60 * 24, lambda n : ungettext('day', 'days', n)),
          (60 * 60 * 60, lambda n: ungettext('hour', 'hours', n)),
          (60 * 60, lambda n: ungettext('minute', 'minutes', n)),
    )

    s = None
    prev = None
    for i, (seconds, name) in enumerate(chunks):
        if prev:
            c = int((ts % prev) / seconds)
        else:
            c = int(ts / seconds)
        prev = seconds
        if c == 0: continue
        if s:
            s += ugettext(', %(number)d %(type)s') % {'number': c, 'type': name(c)}
        else:
            s = ugettext('%(number)d %(type)s') % {'number': c, 'type': name(c)}
    return s

def timesince(d, now=None):
    """
    Takes two datetime objects and returns the time between d and now
    as a nicely formatted string, e.g. "10 seconds".  If d occurs after now,
    then "0 seconds" is returned.

    Units used are years, months, weeks, days, hours, minutes and seconds.
    Microseconds are ignored.  Up to two adjacent units will be
    displayed.  For example, "2 weeks, 3 days" and "1 year, 3 months" are
    possible outputs, but "2 weeks, 3 hours" and "1 year, 5 days" are not.
    """
    chunks = (
      (60 * 60 * 60 * 24 * 365, lambda n: ungettext('year', 'years', n)),
      (60 * 60 * 60 * 24 * 30, lambda n: ungettext('month', 'months', n)),
      (60 * 60 * 60 * 24 * 7, lambda n : ungettext('week', 'weeks', n)),
      (60 * 60 * 60 * 24, lambda n : ungettext('day', 'days', n)),
      (60 * 60 * 60, lambda n: ungettext('hour', 'hours', n)),
      (60 * 60, lambda n: ungettext('minute', 'minutes', n)),
      (60, lambda n: ungettext('second', 'seconds', n))
    )
    # Convert datetime.date to datetime.datetime for comparison.
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    if not now:
        if d.tzinfo:
            now = datetime.datetime.now(LocalTimezone(d))
        else:
            now = datetime.datetime.now()

    # ignore microsecond part of 'd' since we removed it from 'now'
    delta = now - (d - datetime.timedelta(0, 0, d.microsecond))
    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since <= 0:
        # d is in the future compared to now, stop processing.
        return u'0 ' + ugettext('minutes')
    for i, (seconds, name) in enumerate(chunks):
        count = since // seconds
        if count != 0:
            break
    s = ugettext('%(number)d %(type)s') % {'number': count, 'type': name(count)}
    if i + 1 < len(chunks):
        # Now get the second item
        seconds2, name2 = chunks[i + 1]
        count2 = (since - (seconds * count)) // seconds2
        if count2 != 0:
            s += ugettext(', %(number)d %(type)s') % {'number': count2, 'type': name2(count2)}
    return s

if __name__ == "__main__":
    dt = datetime.datetime.now() - datetime.timedelta(seconds=50)
    print timesince(dt)
    
