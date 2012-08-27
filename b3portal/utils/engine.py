import re

def check_guid(engine, guid):
    if engine in ('q3a', 'oa081','iourt41','smg','smg11','etpro','q3a'):
        r = re.match('^[A-F0-9]{32}$', guid) 
    elif engine in ('moh','bfbc2'):
        r = re.match('^EA_[a-f0-9]{32}$', guid, re.IGNORECASE)
    elif engine in ('alt',):
        r = re.match('^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', guid, re.IGNORECASE)
    elif engine and engine.startswith('cod'):
        r = re.match('^[a-f0-9]{32}$', guid)
    else:
        r = False
    return r
