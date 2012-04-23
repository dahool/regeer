# -*- coding: utf-8 -*-
"""Copyright (c) 2010 Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

def open_file(filen):
    if isinstance(filen, basestring):
        return open(filen, 'r')
    return filen

def load_banlist(filen):
    banlist = open_file(filen)
    iplist = banlist.readlines()
    banlist.close()
    lista = set([v.split(':')[0].strip() for v in iplist])
    return lista

def load_banlist_tupple(filen):
    banlist = open_file(filen)
    iplist = banlist.readlines()
    banlist.close()
    lista = []
    for ip in iplist:
        lista.append(create_ip_range_tupple(ip.split(':')[0].strip()))
    lista.sort()
    return lista
    
def load_banlist_all(filen):
    banlist = open_file(filen)
    iplist = banlist.readlines()
    banlist.close()
    lista = set()
    for ip in iplist:
        lista.update(create_ip_range(ip.split(':')[0].strip()))
    return lista

def create_ip_range_tupple(ip):
    parts = ip.split('.')
    if parts[3] == '0':
        start = ip_to_decimal("%s.%s.%s.1" % (parts[0],parts[1],parts[2]))
        end = ip_to_decimal("%s.%s.%s.255" % (parts[0],parts[1],parts[2]))
    else:
        start = ip_to_decimal(ip)
        end = start
    return (start, end)

def create_ip_range(ip):
    parts = ip.split('.')
    iplist = []
    if parts[3] == '0':
        start = ip_to_decimal("%s.%s.%s.1" % (parts[0],parts[1],parts[2]))
        end = ip_to_decimal("%s.%s.%s.255" % (parts[0],parts[1],parts[2]))
        for n in range(start, end + 1):
            iplist.append(decimal_to_ip(n))
    else:
        iplist = [ip]
    return iplist
    
def ip_to_decimal(ip):
    parts = ip.split('.')
    value = 16777216 * int(parts[0]);
    value += 65536 * int(parts[1]);
    value += 256 * int(parts[2]);
    value += int(parts[3]);
    return value

def decimal_to_ip(number):
    ip = "%d.%d.%d.%d" % (number / 256 / 65536,
                          (number / 65536) % 256,
                          (number / 256) % 256,
                          number % 256)
    return ip
    
def save_banlist(filen, lista):
    banlist = open(filen,'w')
    for e in lista:
        banlist.write("%s:-1\n" % e)
    banlist.close()
    
def ip_find_tupple(sublist, value):
    if len(sublist) == 1:
        start, end = sublist[0]
        if value >= start and value <= end:
            return (start, end)
        else:
            return None
    mid = int(len(sublist)/2)
    start, end = sublist[mid]
    if value >= start and value <= end:
        return (start, end)
    if value < start:
        return ip_find_tupple(sublist[:mid], value)
    else:
        return ip_find_tupple(sublist[mid:], value)

        