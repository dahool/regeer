import re

ip_re = re.compile('^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d|[\*])\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d|[\*])\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d|[\*])$')

def is_valid_ip(text):
    return ip_re.match(text)