# WeatherApp

## Description
Here is a sample service that needs to be deployed! You should have recieved a set of credentials that will give you access to an AWS account you can deploy to.

Weather app is a simple service that allows users to signup with an email and location. This email/locatoin is then used to generate personalized emails based on the current weather conditions.

Your mission is to deploy this application using cloudformation. The application will need a database backend (RDS postgres is perfectly acceptable). You should setup the servers to run in an autoscaling group exposed publicly via an ELB.

## Deploying

Django has a checklist worth looking at when trying to deploy: https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/
For the purposes of this excesise, using the built in HTTP server (using manage.py runserver as described in the installing section) is aceptatble when running the application.



## Installing
Weatherapp is written using python (django). To get up and running, first you need to install the python dependencies. I assume you
have a python2.7 interpreters already installed on your machine. I highly recommend you install the dependencies in a virtualenv.
1. Clone the project, navigate to the repository root and execute: `pip install -r requirements.txt`
2. Run the database migrations (I assume you will be using just the sqlite backend. If you want to swap in a different db backend, [consult
the django documentation](https://docs.djangoproject.com/en/1.11/ref/databases/#connecting-to-the-database)): `python manage.py migrate`
3. Populate the locations database: `python manage.py loadlocations`
4. Register for a [wunderground api account](https://www.wunderground.com/weather/api) and set the `WUNDERGROUND_API_KEY` in `/weatherapp/settings.py`
5. (optional) configure your email backend. See the [django documentation regarding email backends](https://docs.djangoproject.com/en/1.11/topics/email/)
6. Run the server `python manage.py runserver` and goto: [http://127.0.0.1:8000](http://127.0.0.1:8000)

The weathermail app is setup to use the django admin panel. To make use of this, you will need to create a superuser account:
1. Create super user account: `python manage.py createsuperuser`
2. Log into the admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Sending Emails
Assuming you have properly configured your email backend, you can send email to subscribers by using the `sendemail` management command:
`python manage.py sendemail`

## Developing
Follow the steps in "Installing" to get a development machine up and running. Execute the unit tests by running: `python manage.py test`
