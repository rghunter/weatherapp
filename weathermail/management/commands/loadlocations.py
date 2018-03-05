from django.core.management.base import BaseCommand, CommandError
from weathermail.models import Location, Subscriber
import sys

import requests

class Command(BaseCommand):
    help = "Bootstraps the location database from opendatasoft.com"

    QUERY = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=1000-largest-us-cities-by-population-with-geographic-coordinates&rows=100&sort=-rank"
    ## The above query pulls the top 100 most populated US cities from opendatasoft database

    def handle(self, *args, **options):
        ## Running this command will delete all existing subscriber records.
        if len(Subscriber.objects.all()) > 0:
            print "Existing subscriber records detected. If you continue running this command, all subscriber records will be deleted."

            resp = raw_input("Are you sure you want to continue? [yes/no]: ")
            if resp != "yes":
                print "Exiting without touching records"
                sys.exit()
        else:
            print "No existing subscriber records found."
        ## First, lets truncate any existing records
        print "Clearing the database"
        Subscriber.objects.all().delete()
        Location.objects.all().delete()

        ## Load cities from opendatasoft
        cities = requests.get(self.QUERY).json()['records']
        for city in cities:
            l = Location.from_opendata_record(city)
            l.save()
            print "Loaded: {}".format(l)


