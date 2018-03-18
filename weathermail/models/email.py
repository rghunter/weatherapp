from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import Context, Template

from enum import Enum

class Subject(Enum):
    GOOD="It's nice out! Enjoy a discount on us."
    NEUTRAL="Enjoy a discount on us."
    BAD="Not so nice out? That's okay, enjoy a discount on us."


class WeatherEmail(object):


    HTML_TEMPLATE = "weathermail/email.html"

    TXT_TEMPLATE = "weathermail/email.txt"

    def __init__(self, from_email):
        self.from_email = from_email

    def send(self, weather_status, temperature, condition, condition_icon, city, state, customer_email):
        """
        Send a weather app email.

        :param weather_status enum Subject: either GOOD, NEUTRAL, BAD depending on how we judge the weather.
        :param temperature float: the outside temperature in F
        :param condition string: a string representing the outside weather conditions
        :param condition_icon string: a url to the icon representing the current weather conditions
        :param city string: the name of the city
        :param state string: the name of the state
        :param email string: email address we are sending this too
        """

        context = dict(
                temperature=temperature,
                condition=condition.lower(), 
                city=city.title(), 
                state=state.upper(), 
                condition_icon=condition_icon)
        html_body = render_to_string(self.HTML_TEMPLATE, context={})
        txt_body = render_to_string(self.TXT_TEMPLATE, context=context)
        send_mail(weather_status.value, txt_body, self.from_email, recipient_list=[customer_email], html_message=html_body)



        
