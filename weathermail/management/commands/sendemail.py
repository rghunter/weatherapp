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
    def average_temp(almanac):
        """
        Wunderground only gives us the average high and low. So what is the average temperature for the day?
        I make the assumption that it is the average of the high and low
        """
        def temp(t):
            return t['normal']['F']
        high = float(temp(almanac['temp_high']))
        low = float(temp(almanac['temp_low']))
        return (high+low)/2.0


    @staticmethod
    def get_subject(weather):

        condition = weather['current_observation']['weather']
        curr_temp = weather['current_observation']['temp_f']

        precipitating = True if float(weather['current_observation']['precip_today_in']) > 0 else False

        avg_temp = Command.average_temp(weather['almanac'])

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

