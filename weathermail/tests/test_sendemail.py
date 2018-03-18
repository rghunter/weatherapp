from django.test import TestCase

import json

from weathermail.management.commands.sendemail import Command
from weathermail.models.email import Subject

class SendemailTest(TestCase):
    """
    Sooo many corner cases:
    In the interest of getting this code challenge done by end of weekend, I had to make a call on a few assumptions regarding corner cases.
    * I assert that wunderground condition Clear and Sunny consitutute "sunny" weather. Any other wunderground condition does not
    * I VERY literally interpreted the algorithim described in the spec for selecting the subject. Idealy the subject states would be evaluated in a transposable order.
    this is not true in the exisitng implementation. For example, what happens if condition is sunny and the temperature is 5 degrees colder than average.
    In my implemnetation, this would be still "good" weather because good weather conditions get evaluated BEFORE bad weather conditions.
    * I defined precipitation as a conditional where 'precip_today_in' > 0.
    """

    @staticmethod
    def gen_almanac(high, low):
        def temp_obj(temp):
            return dict(normal=dict( F=str(temp))) 
        return dict(temp_high=temp_obj(high), temp_low=temp_obj(low))

    def test_gen_almanac(self):
        fix = json.loads("""
        {
            "temp_high": {
                "normal": {
                    "F": "46"
                }
            },
            "temp_low": {
                "normal": {
                    "F": "32"
                }
            }
        }""")
        self.assertEqual(fix, self.gen_almanac(46, 32))
    

    def run_fixture(self, subject_line, test_fixture):
        sub = Command.get_subject(test_fixture)
        self.assertEqual(subject_line, sub)


    def test_good_weather(self):
        ## If its nice out, either sunny (or clear)
        sunny_fixture = dict(
                current_observation=dict(
                    temp_f=10.0,
                    weather="Sunny",
                    precip_today_in="0.0", ## This actually how wunderground represents the data... as as string.. not a float because datatypes (or consistenscy) just dont matter to them ;)
                    ),
                almanac=self.gen_almanac(10, 10)
                )

        self.run_fixture(Subject.GOOD, sunny_fixture)

        clear_fixture = dict(
                current_observation=dict(
                    temp_f=10.0,
                    weather="Clear",
                    precip_today_in="0.0", ## This actually how wunderground represents the data... as as string.. not a float because datatypes (or consistenscy) just dont matter to them ;)
                    ),
                almanac=self.gen_almanac(10, 10)
                )
        
        self.run_fixture(Subject.GOOD, clear_fixture)

        ## or 5 degrees warmer than average
        warm_fixture = dict(
                current_observation=dict(
                    temp_f=15.0,
                    weather="Clear",
                    precip_today_in="0.0", ## This actually how wunderground represents the data... as as string.. not a float because datatypes (or consistenscy) just dont matter to them ;)
                    ),
                almanac=self.gen_almanac(10, 10)
                )


        self.run_fixture(Subject.GOOD, warm_fixture)

    def test_bad_weather(self):
        ## or 5 degrees cooler than average
        cold_fixture = dict(
                current_observation=dict(
                    temp_f=5.0,
                    weather="Clear",
                    precip_today_in="0.0", ## This actually how wunderground represents the data... as as string.. not a float because datatypes (or consistenscy) just dont matter to them ;)
                    ),
                almanac=self.gen_almanac(10, 10)
                )

        self.run_fixture(Subject.BAD, cold_fixture)

        ## or precipitating
        precipitating_fixture = dict(
                current_observation=dict(
                    temp_f=10.0,
                    weather="Something not clear/sunny",
                    precip_today_in="1.0", ## This actually how wunderground represents the data... as as string.. not a float because datatypes (or consistenscy) just dont matter to them ;)
                    ),
                almanac=self.gen_almanac(10, 10)
                )

        self.run_fixture(Subject.BAD, precipitating_fixture)


    def test_neutral_weather(self):

        ## All other conditions are neutral
        neutral_fixture = dict(
                current_observation=dict(
                    temp_f=10.0,
                    weather="Something not clear/sunny",
                    precip_today_in="0.0", ## This actually how wunderground represents the data... as as string.. not a float because datatypes (or consistenscy) just dont matter to them ;)
                    ),
                almanac=self.gen_almanac(10, 10)
                )

        self.run_fixture(Subject.NEUTRAL, neutral_fixture)




        
        



        
