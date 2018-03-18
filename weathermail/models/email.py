from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template import Context, Template

from templated_email import send_templated_mail
from enum import Enum

class Subject(Enum):
    GOOD="It's nice out! Enjoy a discount on us."
    NEUTRAL="Enjoy a discount on us."
    BAD="Not so nice out? That's okay, enjoy a discount on us."


def send_weathermail(weather_status, temperature, condition, condition_icon, city, state, customer_email):
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
    return send_templated_mail(
            template_name="weather",
            from_email="ryan.g.hunter@gmail.com",
            recipient_list=[customer_email],
            context = dict(
                subject=weather_status.value,
                temperature=temperature,
                condition=condition.lower(), 
                city=city.title(), 
                state=state.upper(), 
                condition_icon=condition_icon)
            )
