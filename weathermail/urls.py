from django.conf.urls import url

from .views import SubscriberSignUp, success

urlpatterns = [
    url(r'^success/$', success, name='success'),
    url(r'^$', SubscriberSignUp.as_view(), name='subscribe')
]
