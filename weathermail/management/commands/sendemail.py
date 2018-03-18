import sys
import requests

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from weathermail.models.db import Location, Subscriber
from weathermail.models.wunderground import WundergroundAPI
from weathermail.models.email import send_weathermail, Subject


class Command(BaseCommand):
    help = "Send email to all subscribers"


    @staticmethod
    def get_subject(weather):

        condition = weather['condition']
        curr_temp = weather['temperature']
        avg_temp = weather['average_temp']
        precipitating = weather['precipitating']

        ## If its nice out, either sunny or 5 degrees warmer than average
        if condition in ["Sunny", "Clear"] or (curr_temp - avg_temp) >= 5.0:
            return Subject.GOOD
        ## If its not so nce, either percipitating or 5 degrees cooler than the average temperature
        elif (curr_temp - avg_temp) <= -5.0 or precipitating:
            return Subject.BAD
        ## If the weather does not meet either of those conditions, its an everage weather day
        else:
            return Subject.NEUTRAL


    def handle(self, *args, **options):

        ## Check that the api key is defined. Otherwise throw an error
        if not hasattr(settings, 'WUNDERGROUND_API_KEY'):
            raise ImproperlyConfigured("Could not find WUNDERGROUND_API_KEY in settings.py")

        api_client = WundergroundAPI(settings.WUNDERGROUND_API_KEY)

        for subscriber in Subscriber.objects.all():
            weather = api_client.fetch_data_location(subscriber.location)

            weather_status = self.get_subject(weather)

            print "Email: {}, Weather: {}".format(subscriber, weather_status.name)

            send_weathermail(
                    weather_status,
                    weather['temperature'], 
                    weather['condition'], 
                    weather['condition_icon'], 
                    subscriber.location.city, 
                    subscriber.location.state, 
                    subscriber.email_address)

