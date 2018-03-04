# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Location, Subscriber


admin.site.register(Location)
admin.site.register(Subscriber)

# Register your models here.
