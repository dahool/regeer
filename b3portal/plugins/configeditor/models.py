# -*- coding: utf-8 -*-
"""Copyright (c) 2012 Sergio Gabriel Teves
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
from django.db import models
from b3portal.models import Server
from django.utils.translation import gettext_lazy as _

class ConfigEditorPlugin(models.Model):
    server = models.ForeignKey(Server, related_name="configeditor_plugin", unique=True, verbose_name=_('Server'))
    location = models.CharField(max_length=500, verbose_name=_('B3 Path'),
                                help_text=_('Directory where b3 config is located (parent direcory). We will look for @b3/conf and @b3/extplugins/conf. Local and ftp are supported<br/>For ftp use: ftp://user:password@host:port/file/mapcycle.txt<br/>For http use: http://your.url.com/b3')
                                )

    def __unicode__(self):
        return repr(self)
        
    def __repr__(self):
        return str(self.server)

    class Meta:
        verbose_name = _('Config Editor')
        verbose_name_plural = _('Config Editor')
        db_table = 'plugin_configeditor'