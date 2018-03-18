# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.management import call_command


from weathermail.models.db import Location
from weathermail.management.commands.loadlocations import Command

import requests_mock


class LoadLocationsTest(TestCase):

    sample_request = """
    {
    "nhits": 1000,
    "parameters": {
        "dataset": [
            "1000-largest-us-cities-by-population-with-geographic-coordinates"
        ],
        "timezone": "UTC",
        "rows": 100,
        "sort": [
            "-rank"
        ],
        "format": "json"
    },
    "records": [
        {
            "datasetid": "1000-largest-us-cities-by-population-with-geographic-coordinates",
            "recordid": "eb54a1a661dc616f2dbe5abb166c785044753b0c",
            "fields": {
                "city": "A City",
                "rank": 1,
                "state": "A State",
                "coordinates": [
                    40.7127837,
                    -74.0059413
                ],
                "growth_from_2000_to_2013": 4.8,
                "population": 8405837
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -74.0059413,
                    40.7127837
                ]
            },
            "record_timestamp": "2017-06-01T14:40:33+00:00"
        }
    ]
    }
    """

    @requests_mock.mock()
    def test_command_output(self, m):
        m.get(Command.QUERY, text=self.sample_request)
        call_command('loadlocations')
        locs = Location.objects.all()
        self.assertEqual(len(locs), 1)
        loc = locs[0]
        self.assertEqual(loc.city, "A City")
        self.assertEqual(loc.state, "A State")

