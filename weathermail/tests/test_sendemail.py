from django.test import TestCase

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
    """

    def run_fixture(self, subject_line, test_fixture):
        sub = Command.get_subject(test_fixture)
        self.assertEqual(subject_line, sub)

    def test_good_weather(self):
        ## If its nice out, either sunny (or clear)
        sunny = dict(
                condition="Sunny",
                temperature=10,
                average_temp=10,
                precipitating = False
                )

        self.run_fixture(Subject.GOOD, sunny)
        
        clear = dict(
                condition="Clear",
                temperature=10,
                average_temp=10,
                precipitating = False
                )

        self.run_fixture(Subject.GOOD, clear)

        ## or 5 degrees warmer than average

        five_deg_warmer = dict(
                condition="Clear",
                temperature=15,
                average_temp=10,
                precipitating = False
                )

        self.run_fixture(Subject.GOOD, five_deg_warmer)

    def test_bad_weather(self):
        ## or 5 degrees cooler than average

        five_deg_cooler = dict(
                condition="Raining",
                temperature=5,
                average_temp=10,
                precipitating = False
                )

        self.run_fixture(Subject.BAD, five_deg_cooler)

        ## or precipitating

        precipitating = dict(
                condition="Raining",
                temperature=10,
                average_temp=10,
                precipitating = True 
                )

        self.run_fixture(Subject.BAD, precipitating)


    def test_neutral_weather(self):

        ## All other conditions are neutral

        neutral = dict(
                condition="Raining",
                temperature=10,
                average_temp=10,
                precipitating = False 
                )

        self.run_fixture(Subject.NEUTRAL, neutral)




        
        



        
