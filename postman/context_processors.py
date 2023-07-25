from datetime import datetime
import requests
import json
import environ

env = environ.Env()
environ.Env.read_env()


def login(request):
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

    return  { 'token': token, 'base_url': base_url }


    

def counter(request):

    now = datetime.now()
    year = now.year

    date = now.strftime("%A, %d %B, %Y")

    time = now.strftime("%H:%M %p")

    # print(client_name)
    # print(unlimited)
    

    # return {'total_members': total_members, 'client_name': client_name, 'organization': organization, 'branch':branch, 'unlimited': unlimited, 'date': date, 'time': time, 'year':year, 'new_id':new_id}
    return { 'date': date, 'time': time, 'year':year }


def getClient(request, **kwargs):
    client_id = kwargs.get('client_id')

    return { 'client_id': client_id }
    pass