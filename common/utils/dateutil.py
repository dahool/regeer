from datetime import datetime,timedelta

def datetimeIterator(from_date=None, to_date=None, delta=timedelta(minutes=1)):
    from_date = from_date or datetime.now()
    while to_date is None or from_date <= to_date:
        yield from_date
        from_date = from_date + delta
    return