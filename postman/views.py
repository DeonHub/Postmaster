import csv
import datetime
import io
# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status
# from .serializers import *
from .models import *
# from rest_framework.views import APIView
from postman.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from itertools import chain
import requests
import json
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse

import environ

env = environ.Env()
environ.Env.read_env()


base_url = "https://db-api-v2.akwaabasoftware.com"

login_url = base_url + "/clients/login"

payload = json.dumps({
"phone_email": env('EMAIL'),
"password": env('PASSWORD')
})


headers = {
'Content-Type': 'application/json',
'Cookie': 'csrftoken=UN5qKQ1rbg40wB0OWDXyWbO612Lvx41Bb2o0xCYkNfcrhrdvUpxgSYkXDBneGvMT; sessionid=ij0kr81ryje5mijdenssrwt3coffqw4z'
}

response = requests.request("POST", login_url, headers=headers, data=payload).json()
token = response['token']



# Create your views here.
def webpage(request, message_id):
    
    template_name = 'api/websms.html'

    webmail = Post.objects.get(message_id=message_id)

    return render(request, template_name, {
        'post': Post.objects.all(),
        'webmail': webmail
    })


def index(request):
    template_name = 'postman/index.html'

    return render(request, template_name, {

    })


def dashboard(request, client_id):
    template_name = 'postman/dashboard.html'

    client_url = f'{base_url}/account?id={client_id}'

    payload = json.dumps({})

    headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=i0QCkPPQCUAYcsvB4MvYAfzl4HrLL0GJ'
    }


    try:
        response = requests.request("GET", client_url, headers=headers, data=payload).json()['results'][0]
        client = response['name']
    except:
        client = "No one"    

    # client_id = kwargs.get(client_id)
    # branch = kwargs.get(branch)

    return render(request, template_name, {
        'id': client

    })





# def link(request, contact, message_id):
#         base_url = "http://127.0.0.1:8000/"
#         link = base_url + f'client/pay-public-donation/{public_donation.id}'

#         shortener = pyshorteners.Shortener()
#         payment_link = shortener.tinyurl.short(link)




# Create Fee types
def createServiceType(request):
    # admin = user['firstname'] +' '+ user['surname']
    template_name = 'postman/create-service-type.html'

    if request.method == 'POST':
        services = request.POST.get('services')
        unit_amount_usd = request.POST.get('unit_amount_usd')
        unit_amount_ghs = request.POST.get('unit_amount_ghs')

        if unit_amount_ghs == "":
            unit_amount_ghs = 1

        if ',' in services:
            services = services.split(',')

            for service in services:
                fee_type = ServiceTypes(service_type=service, unit_amount_usd=unit_amount_usd, unit_amount_ghs=unit_amount_ghs)
                fee_type.save()

            activity = ActivityLog(user="Admin", action=f'created fee type(s) {",".join(services)}')    
            activity.save()
        else:
            fee_type = ServiceTypes(service_type=services, unit_amount_usd=unit_amount_usd, unit_amount_ghs=unit_amount_ghs)
            fee_type.save()

            activity = ActivityLog(user="Admin", action=f'created fee type {services}')    
            activity.save()

        messages.success(request, 'Service Type(s) created successfully!')
        return HttpResponseRedirect(reverse('postman:viewServiceTypes')) 
    else:
        return render(request, template_name, {

        })




# View fee type

def viewServiceTypes(request):

    template_name = 'postman/view-service-types.html'
    services = ServiceTypes.objects.all()
    return render(request, template_name, {
        'services': services
    })



# Edit fee type
def editServiceType(request, id):

    template_name = 'postman/edit-service-type.html'
    service_type = ServiceTypes.objects.get(id=id)
    
    if request.method == 'POST':
        service_type.service_type = request.POST.get('service_type')
        service_type.unit_amount_usd = request.POST.get('unit_amount_usd')
        service_type.unit_amount_ghs = request.POST.get('unit_amount_ghs')
        service_type.save()

        activity = ActivityLog(user="Admin", action=f'edited fee type {service_type}')    
        activity.save()

        messages.success(request, 'Service Type edited successfully!')

        return HttpResponseRedirect(reverse('postman:viewServiceTypes')) 


    return render(request, template_name, {
        'service': service_type,
        'services': ServiceTypes.objects.all(),
    }) 





# Delete fee type
def deleteServiceType(request, id, *args, **kwargs):

    if request.method == "POST":
        service_type = ServiceTypes.objects.get(id=id)
        service_type.delete()

        activity = ActivityLog(user="Admin", action=f'deleted service type {service_type}')    
        activity.save()

    messages.success(request, 'Service Type deleted successfully!')
    return HttpResponseRedirect(reverse('postman:viewServiceTypes')) 


    
