from django.core.management.base import BaseCommand, CommandError
from weathermail.models import Location

import requests

class Command(BaseCommand):
    help = "Bootstraps the location database from opendatasoft.com"

    QUERY = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=1000-largest-us-cities-by-population-with-geographic-coordinates&rows=100&sort=-rank"

    def handle(self, *args, **options):
        ## First, lets truncate any existing records
        Location.objects.all().delete()

        ## Load cities from opendatasoft
        cities = requests.get(self.QUERY).json()['records']
        for city in cities:
            l = Location.from_opendata_record(city)
            l.save()
            print "Loaded: {}".format(l)


