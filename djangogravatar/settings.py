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
from django.conf import settings as main_settings

GRAVATAR_URL=getattr(main_settings, 'GRAVATAR_URL','http://www.gravatar.com/')
GRAVATAR_SIZE=getattr(main_settings, 'GRAVATAR_SIZE','32')
# mm: (mystery-man) a simple, cartoon-style silhouetted outline of a person (does not vary by email hash)
# identicon: a geometric pattern based on an email hash
# monsterid: a generated 'monster' with different colors, faces, etc
# wavatar: generated faces with differing features and backgrounds
GRAVATAR_DEFAULT=getattr(main_settings, 'GRAVATAR_DEFAULT','wavatar')