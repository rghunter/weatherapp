# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError

import json



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

    def test_import(self):
        sample_object = json.loads("""
        {
            "datasetid": "1000-largest-us-cities-by-population-with-geographic-coordinates",
            "recordid": "29df7b4e3a881a99657fd285cd041fe204917083",
            "fields": {
                "city": "Los Angeles",
                "rank": 2,
                "state": "California",
                "coordinates": [
                    34.0522342,
                    -118.2436849
                ],
                "growth_from_2000_to_2013": 4.8,
                "population": 3884307
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -118.2436849,
                    34.0522342
                ]
            },
            "record_timestamp": "2017-06-01T14:40:33+00:00"
        }
        """)
        location = Location.from_opendata_record(sample_object)

        self.assertEqual(location.city, "Los Angeles")
        self.assertEqual(location.state, "California")



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

