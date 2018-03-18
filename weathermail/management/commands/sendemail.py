from django.core.management.base import BaseCommand, CommandError
from weathermail.models.db import Location, Subscriber
from weathermail.models.wunderground import WundergroundAPI
from weathermail.models.email import send_weathermail, Subject
import sys

import requests

class Command(BaseCommand):
    help = "Send email to all subscribers"


    def get_subject(self, condition, curr_temp, avg_temp):
        ## Fill out controller
        return Subject.GOOD


    def handle(self, *args, **options):
        api_client = WundergroundAPI("f586ab242103273e")
        for subscriber in Subscriber.objects.all():
            weather = api_client.fetch_data_location(subscriber.location)
            send_weathermail(
                    self.get_subject(
                        weather['condition'], 
                        weather['temperature'], 
                        weather['average_temp']),
                    weather['temperature'], 
                    weather['condition'], 
                    weather['condition_icon'], 
                    subscriber.location.city, 
                    subscriber.location.state, 
                    subscriber.email_address)

