from datetime import datetime
import requests
import json
import environ

env = environ.Env()
environ.Env.read_env()



def counter(request):

    now = datetime.now()
    year = now.year

    date = now.strftime("%A, %d %B, %Y")

    time = now.strftime("%H:%M %p")


    # return {'total_members': total_members, 'client_name': client_name, 'organization': organization, 'branch':branch, 'unlimited': unlimited, 'date': date, 'time': time, 'year':year, 'new_id':new_id}
    return { 'date': date, 'time': time, 'year':year }
