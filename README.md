# WeatherApp

## Description
Implementation of Klavio's https://www.klaviyo.com/weather-app sample project

## Installing
Weatherapp is written using python (django). To get up and running, first you need to install the python dependencies. I assume you
have a python2.7 interpreters already installed on your machine. I highly recommend you install the dependencies in a virtualenv.
1. Clone the project, navigate to the repository root and execute: `pip install -r requirements.txt`
2. Run the database migrations (I assume you will be using just the sqlite backend. If you want to swap in a different db backend, [consult
the django documentation](https://docs.djangoproject.com/en/1.11/ref/databases/#connecting-to-the-database)): `python manage.py migrate`
3. Populate the locations database: `python manage.py loadlocations`
4. Register for a [wunderground api account](https://www.wunderground.com/weather/api) and set the `WUNDERGROUN_API_KEY` in `/weatherapp/settings.py`
5. (optional) configure your email backend. See the [django documentation regarding email backends](https://docs.djangoproject.com/en/1.11/topics/email/)
6. Run the server `python manage.py runserver` and goto: [http://127.0.0.1:8000](http://127.0.0.1:8000)

The weathermail app is setup to use the django admin panel. To make use of this, you will need to create a superuser account:
1. Create super user account: `python manage.py createsuperuser`
2. Log into the admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Sending Emails
Assuming you have properly configured your email backend, you can send email to subscribers by using the `sendemail` management command:
`python manage.py sendemail`

## Assumptions Made
I had to make a number of assumptions when implementing the controller for sending emails. see: https://github.com/rghunter/weatherapp/blob/master/weathermail/tests/test_sendemail.py for more detail
In a perfect world, I would prefer to actually talk these corner cases through with whoever wrote the specification; however, I elected to make a call on my own
and document the assumptions I made rather than drag the project out another weekend. 

## Developing
Follow the steps in "Installing" to get a development machine up and running. Execute the unit tests by running: `python manage.py test`
