# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from .models import Location, Subscriber

class LocationTestCase(TestCase):

    def test_display_value(self):
        """
        Disaplay value for amodel object should follow city, state
        """
        l = Location(city="Boston", state="MA")
        self.assertEqual(str(l), "Boston, MA")
