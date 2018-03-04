# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError



from .models import Location, Subscriber

class LocationTestCase(TestCase):

    def test_display_value(self):
        """
        Disaplay value for amodel object should follow city, state
        """
        l = Location(city="Boston", state="MA")
        self.assertEqual(str(l), "Boston, MA")

    def test_unique(self):
        """
        Test that we get an error if we try to add the same city twice. We expect an Integrity Error
        """
        Location(city="Boston", state="MA").save()
        with self.assertRaises(IntegrityError):
            Location(city="Boston", state="MA").save()


class SubsriberTestCase(TestCase):

    def setUp(self):
        self.location = Location(city="Boston", state="MA")
        self.location.save()

    def test_email_validation(self):
        with self.assertRaises(ValidationError):
            Subscriber(location=self.location, email_address="ryan.g.hunter").clean_fields()


    def test_unique_email(self):
        """
        Test that we get an integrity error if we try and save the same email twice
        """
        Subscriber(location=self.location, email_address="ryan.g.hunter@gmail.com").save()
        with self.assertRaises(IntegrityError):
            Subscriber(location=self.location, email_address="ryan.g.hunter@gmail.com").save()

