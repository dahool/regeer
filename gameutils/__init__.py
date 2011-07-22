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
def load_banlist(file):
    banlist = open(file)
    iplist = banlist.readlines()
    banlist.close()
    list = set([v.split(':')[0].strip() for v in iplist])
    return list

def save_banlist(file, list):
    banlist = open(file,'w')
    for e in list:
        banlist.write("%s:-1\n" % e)
    banlist.close()