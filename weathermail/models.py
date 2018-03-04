# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    def __unicode__(self):
        return "{}, {}".format(self.city, self.state)

    class Meta:
        unique_together = ('city', 'state')  ## prevent us from accidently adding a city/state combo twice


class Subscriber(models.Model):
    email_address = models.EmailField(unique=True)  # eforce requirement that email cannot be registered multiple times
    location = models.ForeignKey(Location)
