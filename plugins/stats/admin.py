# -*- coding: utf-8 -*-
from django.contrib import admin
from b3connect.admin import CustomModelAdmin
from models import KnifeStat, NaderStat, FlagStat

admin.site.register(KnifeStat, CustomModelAdmin)
admin.site.register(NaderStat, CustomModelAdmin)
admin.site.register(FlagStat, CustomModelAdmin)
