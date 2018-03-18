from .models.db import Subscriber 
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render



class SubscriberSignUp(CreateView):
    model = Subscriber
    fields = '__all__'
    success_url = reverse_lazy('success')


def success(request):
    return render(request, 'weathermail/success.html')
