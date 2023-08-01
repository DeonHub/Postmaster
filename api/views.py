import csv
import datetime
import io
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.views import APIView
from postman.models import Post, ContactGroups, ServiceTypes, TopUps, Credits
import requests
import json
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import render, get_object_or_404
import pyshorteners
import environ


env = environ.Env()
environ.Env.read_env()



def remove_non_numeric(string):
    return ''.join(filter(str.isdigit, string))


def makePayment(description, amount_paid, order_id):

    url = "https://payproxyapi.hubtel.com/items/initiate"

    returnUrl = f"https://akwaabasoftware.com/"


    payload = json.dumps({
            "totalAmount": amount_paid,
            "description": description,
            "callbackUrl": "https://transactions.akwaabasoftware.com/add-transaction/",
            "returnUrl": returnUrl,
            "merchantAccountNumber": "2017254",
            "cancellationUrl": "https://hubtel.com/",
            "clientReference": order_id
        })


    headers = {
    'Authorization': 'Basic UDc5RVdSVzozNmZmNzk3YTgyMjU0NzJmOTA2ZGU0NGM3NGVkZWE0Zg==',
    'Content-Type': 'application/json'
    }


    response = requests.request("POST", url, headers=headers, data=payload).json()['data']['checkoutUrl']

    return response
    






class SetEmailDetails(APIView):
    
    def post(self, request, *args):

        today = datetime.date.today()
        year = datetime.datetime.now().year
        year = str(year) + "0000"

        members = EmailSerializer(data=request.data)

        if members.is_valid():
            client_id = members.data['client_id']
            branch = members.data['branch']
            email = members.data['email']
            password = members.data['password']

            client_emails = ClientEmails.objects.create( client_id=client_id, branch=branch, email=email, password=password )
            client_emails.save()

            data = {
                "success": True,
                "msg": "Client email set successfully",
             }

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(members.errors, status=status.HTTP_400_BAD_REQUEST)  



class ContactGroup(APIView):

    def get_contact_by_pk(self, pk):
    
        try:
            return ContactGroups.objects.get(pk=pk)
        except ContactGroups.DoesNotExist:
            return Response({
                "error": "Duty does not exist"
            }, status=status.HTTP_404_NOT_FOUND)   



    # def delete(self, request, pk):

    #     contact = self.get_contact_by_pk(pk)
    #     contact.delete()

    #     error = {
    #             "success": True,
    #             "message": "Contact deleted successfully"
    #             }
    #     return Response(error, status=status.HTTP_400_BAD_REQUEST) 
 

    def get(self, request, **kwargs):
    
        client_id=kwargs.get('client_id')
        branch=kwargs.get('branch')

        all_heroes = ContactGroups.objects.filter(client_id=client_id, branch=branch)
        heroes = ContactGroupSerializer(all_heroes, many=True)

        info = {
            "count" : len(ContactGroups.objects.all()),
            "data": heroes.data
        }
        
        return Response(info)



    def post(self, request, *args):
        new_group = GroupSerializer(data=request.data)
        today = datetime.date.today()


        if new_group.is_valid():
            client_id = new_group.data['client_id']
            branch = new_group.data['branch']
            group_name = new_group.data['group_name']

            try:
                data = request.FILES['data']
                file = new_group.data['file']

                if not file.name.endswith('.csv'):
                    return Response({
                        "error": "File selected is not a CSV"
                    }, status=status.HTTP_404_NOT_FOUND)  

                try:
                    data_set = file.read().decode('UTF-8')
                    io_string = io.StringIO(data_set)
                    next(io_string)

                    for column in csv.reader(io_string, delimiter=",", quotechar="|"):
                        _, created = ContactGroups.objects.update_or_create(
                                    client_id=client_id,
                                    branch=branch,
                                    group_name=group_name,
                                    firstname=column[0],
                                    othername=column[1],
                                    email=column[2],
                                    contact=column[3],
                                    sent_by="Admin"
                        )

                    data = {
                            "success": True,
                            "message": "Contact group created successfully",
                        }

                    return Response(data, status=status.HTTP_200_OK)

                except csv.Error as e:
                    raise Exception(e)    

            except Exception as e:
                raise Exception("You need to provide a file ")
                       
        else:    
            return Response(new_group.errors, status=status.HTTP_400_BAD_REQUEST)  



class TopUpCredit(APIView):

    def post(self, request, *args):
        now = datetime.datetime.now()
        year = datetime.datetime.now().year
        year = str(year) + "0000"
        
        info = TopUpSerializer(data=request.data)

        if info.is_valid():
            client_id=info.data['client_id']
            branch=info.data['branch']
            service_type=info.data['service_type']
            amount_paid = float(info.data['amount_paid'])


            order_id = remove_non_numeric(str(now))

            top_ups = TopUps.objects.create(client_id=client_id, service_type=service_type.lower(), branch=branch, amount_paid=amount_paid, order_id=order_id)
            top_ups.save()


            description = f"Top up {service_type} credits"

            resp = makePayment(description, amount_paid, order_id)


            data = {
                "success": True,
                "order_id": order_id,
                "payment_url": resp   
                }   

            return Response(data, status=status.HTTP_200_OK)

        else:    
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)     



class AddCredit(APIView):
    
    def post(self, request, *args):

        info = AddCreditSerializer(data=request.data)

        if info.is_valid():

            client_id=info.data['client_id']
            order_id=info.data['order_id']
            branch=info.data['branch']
            service_type=info.data['service_type']

            url = f"https://transactions.akwaabasoftware.com/transactions/{order_id}/"
            payload = {}
            headers = {}

            paid = requests.request("GET", url, headers=headers, data=payload).json()['success']

            if paid == True:

                try:
                    credit = TopUps.objects.get(order_id=order_id)

                    if credit.confirmed:

                        data = {
                            "msg": "Order has already been confirmed",
                            "order_id": order_id
                        } 
                        return Response(data, status=status.HTTP_200_OK)
                    
                    else:
                        
                        amount_paid = float(credit.amount_paid)
                        
                        service = ServiceTypes.objects.filter(service_type=service_type).first()

                        available = float(amount_paid) // float(service.unit_amount_ghs)

                        available = int(available)
                        
                        try:
                            cred = Credits.objects.get(client_id=client_id, service_type=credit.service_type, branch=credit.branch)
                            cred.available_units += available 
                            cred.save()

                        except:
                            print("In exvept")
                            cred = Credits.objects.create(client_id=client_id, service_type=credit.service_type, branch=credit.branch, available_units=available)
                            cred.save() 


                        credit.confirmed = True  
                        credit.save() 

                        data = {
                            "success": True,
                            "msg": f"{credit.service_type} credit updated successfully",
                            "order_id": order_id
                        } 

                        return Response(data, status=status.HTTP_200_OK)

                        
                except:
                    data = {
                        "success": False,
                        "msg": "Purchase does not exist.",
                    }   

                    return Response(data, status=status.HTTP_200_OK)   
            
            else:
                data = {
                    "success": False,
                    "msg": "Purchase does not exist. Please try again after sometime or contact admin", 
                }   

                return Response(data, status=status.HTTP_400_BAD_REQUEST)  
        else:    
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)    



class PurchaseHistory(APIView):
    
    def get(self, request, *args, **kwargs):
        
        client_id=kwargs.get('client_id')
        branch=kwargs.get('branch')

        top_ups = TopUps.objects.filter(client_id=client_id, branch=branch, confirmed=True)
        heroes = PurchaseHistorySerializer(top_ups, many=True)

        info = {
            "count" : len(top_ups),
            "data": heroes.data
        }
        
        return Response(info, status=status.HTTP_200_OK)




class GetCredits(APIView):
    
    def get(self, request, *args, **kwargs):
        
        client_id=kwargs.get('client_id')
        branch=kwargs.get('branch')
        data = []

        try:

            credits = Credits.objects.filter(client_id=client_id, branch=branch)
            
            if credits:
                for credit in credits:
                    data.append({
                        "service_type": credit.service_type,
                        "available_units": credit.available_units
                    }) 

            else:
                pass

            info = {
                    "success": True,
                    "data": data
                    }   

            return Response(info, status=status.HTTP_200_OK)
            

        except:
            info = {
                "success" : False,
                "msg": "Invalid client id or branch"
            }
            
            return Response(info)   




class GetPosts(APIView):
    
    def get(self, request, **kwargs):

        client_id=kwargs.get('client_id')
        branch=kwargs.get('branch')

        all_heroes = Post.objects.filter(client_id=client_id, branch=branch)
        heroes = PostsSerializer(all_heroes, many=True)

        info = {
            "count" : len(Post.objects.all()),
            "data": heroes.data
        }
        
        return Response(info)



# Getting all assigned duties
class SendPosts(APIView):

    def post(self, request, *args):

        new_post = PostSerializer(data=request.data)
        year = datetime.datetime.now().year
        today = datetime.datetime.now()
        year = str(year) + "0000"

        if new_post.is_valid():
            message_type=new_post.data['message_type']
            client_id=new_post.data['client_id']
            branch=new_post.data['branch']
            schedule=new_post.data['schedule']
            recurring=new_post.data['recurring']

            if message_type != "":

                if message_type == "sms" or message_type == "SMS":
                    contacts=new_post.data['contacts']

                    if contacts != "":
                        if ',' in contacts:
                            all_contacts = contacts.split(',')
                            total_conts = len(all_contacts)
                        else:
                            all_contacts = [contacts]
                            total_conts = 1 

                        total_contacts = int(total_conts)  
                        # sending_numbers = (",").join([str(x) for x in (all_contacts + group_contacts)])
                        sending_numbers = (",").join([str(x) for x in (all_contacts)])
                        # senders_numbers = all_contacts + group_contacts
                        senders_numbers = all_contacts    


                    else:
                        contacts = None        

                    main_message=new_post.data['main_message']

                    if main_message != "":
                        total_characters = len(main_message)
                    else:
                        main_message=None

                if "email" in message_type:
                    emails=new_post.data['emails']
                    subject=new_post.data['subject']
                    main_message=new_post.data['main_message']

                    if main_message != "":
                        total_characters = len(main_message)

                    if emails != "":
                        if ',' in emails:
                            all_emails = emails.split(',')
                            total_mails = len(all_emails)
                        else:
                            all_emails = [emails]
                            total_mails = 1 

                        # total_emails = int(group)+int(total_mails)  
                        total_emails = int(total_mails)  
                        # sending_emails = group_emails + all_emails

                        sending_emails = all_emails

                        
                if "audio" in message_type:
                    audio_url=new_post.data['audio_url']
                    contacts=new_post.data['contacts']


                    if ',' in contacts:
                        all_contacts = contacts.split(',')
                        total_conts = len(all_contacts)
                    else:
                        all_contacts = [contacts]
                        total_conts = 1 

                    total_contacts = int(total_conts)  
                    # sending_numbers = (",").join([str(x) for x in (all_contacts + group_contacts)])
                    sending_numbers = (",").join([str(x) for x in (all_contacts)])
                    # senders_numbers = all_contacts + group_contacts
                    senders_numbers = all_contacts                     


                if "websms" in message_type:
                    contacts=new_post.data['contacts']
                    web_message=new_post.data['web_message']
                    main_message=new_post.data['main_message']

                    if main_message != "":
                        total_characters = len(main_message)
                    else:
                        main_message=None

                    if contacts != "":
                        if ',' in contacts:
                            all_contacts = contacts.split(',')
                            total_conts = len(all_contacts)
                        else:
                            all_contacts = [contacts]
                            total_conts = 1 

                        total_contacts = int(total_conts)  
                        # sending_numbers = (",").join([str(x) for x in (all_contacts + group_contacts)])
                        sending_numbers = (",").join([str(x) for x in (all_contacts)])
                        # senders_numbers = all_contacts + group_contacts
                        senders_numbers = all_contacts    


                    else:
                        contacts = None  

                    try:
                        image_url=new_post.data['image_url']
                        file=new_post.data['file']
                    except:
                        image_url = None
                        file = None   

            if schedule == "True":
                schedule_date=new_post.data['schedule_date']
                schedule_time=new_post.data['schedule_time']
            else:
                schedule_date=None
                schedule_time=None

            if recurring == "True":
                recurring_period=new_post.data['recurring_period']
            else:
                recurring_period=None   



            try:
                description= new_post.data['description']
                # print(description)

                description_type= new_post.data['description_type']
            except:
                description = None
                description_type = None   
              

            try:
                personalize=new_post.data['personalize']
            except:
                personalize=None


            try:
                contact_group=new_post.data['contact_group']

                if contact_group != "":
                    try:
                        group = ContactGroups.objects.filter(group_name=contact_group).count()
                        group_contacts = [x.contact for x in ContactGroups.objects.filter(group_name=contact_group)]
                        group_emails = [x.email for x in ContactGroups.objects.filter(group_name=contact_group)]
                    except:
                        group = 0 
                        group_contacts = []
                        group_emails  = [] 
            except:    
                contact_group=None
               
            try:
                draft=new_post.data['draft']
            except:
                draft=False    
                

            
 
            # print(subject)
            try:
                # Available sms
                temp_sms = Credits.objects.get(client_id=client_id, branch=branch, service_type="SMS" or "sms")
                available_sms = temp_sms.available_units
            except:
                available_sms = 0

            try:    
                temp_email = Credits.objects.get(client_id=client_id, branch=branch, service_type="Email" or "email")
                available_email = temp_email.available_units
            except:
                available_email = 0

            try:
                temp_audio = Credits.objects.get(client_id=client_id, branch=branch, service_type="Audio" or "audio")
                available_audio = temp_audio.available_units
            except:
                available_audio = 0


            try:    
                temp_websms = Credits.objects.get(client_id=client_id, branch=branch, service_type="WebSMS" or "websms")
                available_websms = temp_websms.available_units
            except:
                available_websms = 0



            # temp_sms = Credits.objects.get(client_id=client_id, branch=branch, service_type="SMS")
            # available_sms = temp_sms.available_units

            # temp_email = Credits.objects.get(client_id=client_id, branch=branch, service_type="Email")
            # available_email = temp_email.available_units

            # temp_audio = Credits.objects.get(client_id=client_id, branch=branch, service_type="Audio")
            # available_audio = temp_audio.available_units

            # temp_websms = Credits.objects.get(client_id=client_id, branch=branch, service_type="WebSMS")
            # available_websms = temp_websms.available_units










                   

            # total_contacts = int(group)+int(total_conts)  


            # print(senders_numbers)    




            # print(sending_emails)






            added_post = Post.objects.create(
                                    message_type=message_type,
                                    client_id=client_id,
                                    branch=branch,
                                    # description=description,
                                    # description_type=description_type,
                                    schedule=schedule,
                                    # schedule_date=schedule_date,
                                    # schedule_time=schedule_time,
                                    # personalize=personalize,
                                    # contacts=contacts,
                                    # emails=emails,
                                    # contact_group=contact_group,
                                    recurring=recurring,
                                    # recurring_period=recurring_period,
                                    # subject=subject,
                                    # main_message=main_message,
                                    # draft=draft,
                                    # web_message=web_message,
                                    # image=image_url,
                                    # file=file,
                                    # audio_file=audio_url,
                                    # total_contacts=total_contacts,
                                    # total_characters=total_characters,
                                )

            added_post.save()

            message_id = f'PMI{int(year)+added_post.id}'
            added_post.message_id = message_id  

            added_post.save() 




            if added_post.message_type == "sms" or added_post.message_type == "SMS":
                added_post.contacts = contacts
                added_post.main_message = main_message
                added_post.total_contacts = total_contacts
                added_post.total_characters = total_characters
                added_post.save() 

            elif "email" in added_post.message_type: 
                added_post.emails = emails
                added_post.subject = subject
                added_post.main_message = main_message
                added_post.total_emails = total_emails 
                added_post.save() 

            elif "audio" in added_post.message_type:
                added_post.audio_url = audio_url
                added_post.contacts = contacts
                added_post.total_contacts = total_contacts
                added_post.save()

            elif "websms" in message_type:
                added_post.contacts = contacts
                added_post.main_message = main_message
                added_post.total_contacts = total_contacts
                added_post.total_characters = total_characters
                added_post.web_message = web_message
                added_post.image_url = image_url
                added_post.file = file
                added_post.save() 

            if added_post.schedule == True:
                added_post.schedule_date = schedule_date
                added_post.schedule_time = schedule_time
                added_post.save() 












            if draft == "True":

                added_post.draft = True
                added_post.save() 

                info = {
                    "success": True,
                    "msg": "Message(s) saved as draft"
                }


            else:
                if schedule == "True":

                    if today <= schedule_date:

                        if message_type == "sms" or message_type == "SMS":

                                if int(available_sms) >= len(senders_numbers):
            
                                    url = env('SMS_URL')

                                    payload = json.dumps({
                                            "privatekey": env('SMS_PRIVATE_KEY'),
                                            "publickey": env('SMS_PUBLIC_KEY'),
                                            "sender": env('SENDERS_ID'),
                                            "numbers": sending_numbers,
                                            "message": main_message
                                        })

                                    headers = {
                                    'Content-Type': 'application/json'
                                    }

                                    send_sms = requests.request("POST", url, headers=headers, data=payload).json()
                                    # print(send_sms)

                                    if send_sms['status'] == 1000:
                                        
                                        temp_sms.available_units -= len(senders_numbers)
                                        temp_sms.save()

                                        info = {
                                                "success": True,
                                                "msg": "Message(s) sent successfully"
                                            }

                                        return Response(info, status=status.HTTP_200_OK) 

                                    else:
                                        info = {
                                                "success": False,
                                                "msg": "Server error"
                                            }

                                        return Response(info, status=status.HTTP_200_OK)                                 


                                else:
                                    info = {
                                        "success": False,
                                        "msg": f"Insufficient balance. You can only send to {temp_sms.available_units} contact(s)"
                                    }

                                    return Response(info, status=status.HTTP_400_BAD_REQUEST)


                        elif "email" in message_type:

                            if int(available_email) >= len(sending_emails):
    
                                senders_mail = settings.EMAIL_HOST_USER
                                
                                email = EmailMessage(subject, main_message, senders_mail, sending_emails)

                                try:
                                    email.send()
                                    temp_email.available_units -= len(sending_emails)
                                    temp_email.save()

                                    info = {
                                            "success": True,
                                            "msg": "Message(s) sent successfully"
                                        }

                                    return Response(info, status=status.HTTP_200_OK) 

                                except: 
                                    print("Server error")
                                    pass

                                    info = {
                                            "success": False,
                                            "msg": "Server error"
                                        }

                                    return Response(info, status=status.HTTP_400_BAD_REQUEST)  

                            else:
                                info = {
                                    "success": False,
                                    "msg": f"Insufficient balance. You can only send to {temp_email.available_units} emails"
                                }

                                return Response(info, status=status.HTTP_400_BAD_REQUEST)



                        elif "audio" in message_type:

                            if int(available_audio) >= len(senders_numbers):
    
                                url = env('AUDIO_URL')

                                payload = json.dumps({
                                "id": env('SENDERS_ID'),
                                "caller_id": env('CALLERS_ID'),
                                "recipient": senders_numbers,
                                "media_url": audio_url,
                                "direction": env('DIRECTION')
                                })

                                headers = {
                                'Authorization': env('AUDIO_API_KEY'),
                                'Content-Type': 'application/json'
                                }

                                response = requests.request("POST", url, headers=headers, data=payload).json()
                                # print(response)


                                temp_audio.available_units -= len(senders_numbers)
                                temp_audio.save()


                                info = {
                                        "success": True,
                                        "msg": "Message(s) sent successfully"
                                    }

                                return Response(info, status=status.HTTP_200_OK)  
                            
                            else:
                                info = {
                                    "success": False,
                                    "msg": f"Insufficient balance. You can only send to {temp_audio.available_units} contacts"
                                }

                                return Response(info, status=status.HTTP_400_BAD_REQUEST)
                            

                            # if int(available_audio) > 0:

                            #     url = env('AUDIO_URL')

                            #     payload = json.dumps({
                            #     "id": env('SENDERS_ID'),
                            #     "caller_id": env('CALLERS_ID'),
                            #     "recipient": senders_numbers,
                            #     "media_url": audio_url,
                            #     "direction": env('DIRECTION')
                            #     })

                            #     headers = {
                            #     'Authorization': env('AUDIO_API_KEY'),
                            #     'Content-Type': 'application/json'
                            #     }

                            #     response = requests.request("POST", url, headers=headers, data=payload).json()

                            #     temp_audio.available_units -= len(senders_numbers)
                            #     temp_audio.save()

                            #     info = {
                            #             "success": True,
                            #             "msg": "Message(s) sent successfully"
                            #         }

                            #     return Response(info, status=status.HTTP_200_OK) 
                            
                            # else:
                            #     info = {
                            #         "success": False,
                            #         "msg": "Insufficient balance to complete audio request"
                            #     }

                            #     return Response(info, status=status.HTTP_400_BAD_REQUEST)


                        elif "websms" in message_type:

                            if int(available_websms) >= len(senders_numbers):
    
                                url = env('SMS_URL')

                                for i in senders_numbers:
                                    base_url = "https://postmaster.akwaabasoftware.com/"
                                    sid = f'{int(year)+added_post.id}'
                                    weblink = base_url + f'api/websms/{sid}/t={i}'

                                    sending_mail = main_message+"\n"+weblink

                                    payload = json.dumps({
                                    "privatekey": env('SMS_PRIVATE_KEY'),
                                    "publickey": env('SMS_PUBLIC_KEY'),
                                    "sender": env('SENDERS_ID'),
                                    "numbers": i,
                                    "message": sending_mail
                                    })

                                    headers = {
                                    'Content-Type': 'application/json'
                                    }

                                    send_sms = requests.request("POST", url, headers=headers, data=payload).json()

                                    if send_sms['status'] == 1000:
                                        temp_websms.available_units -= 1
                                        temp_websms.save()

                                info = {
                                        "success": True,
                                        "msg": "Message(s) sent successfully"
                                    }

                                return Response(info, status=status.HTTP_200_OK)             
                            else:
                                info = {
                                    "success": False,
                                    "msg": "Insufficient balance. You can only send to {temp_websms.available_units} contacts"
                                }

                                return Response(info, status=status.HTTP_400_BAD_REQUEST) 

                            # if int(available_websms) > 0:

                            #     url = env('SMS_URL')

                            #     for i in senders_numbers:
                            #         base_url = "http://127.0.0.1:8000/"
                            #         sid = f'{int(year)+added_post.id}'
                            #         weblink = base_url + f'api/websms/{sid}/t={i}'

                            #         sending_mail = main_message+"\n"+weblink

                            #         payload = json.dumps({
                            #         "privatekey": env('SMS_PRIVATE_KEY'),
                            #         "publickey": env('SMS_PUBLIC_KEY'),
                            #         "sender": env('SENDERS_ID'),
                            #         "numbers": i,
                            #         "message": sending_mail
                            #         })

                            #         headers = {
                            #         'Content-Type': 'application/json'
                            #         }

                            #         send_sms = requests.request("POST", url, headers=headers, data=payload).json()

                            #         if send_sms['status'] == 1000:
                            #             available_websms -= 1


                            #     info = {
                            #             "success": True,
                            #             "msg": "Message(s) sent successfully"
                            #         }

                            #     return Response(info, status=status.HTTP_200_OK)  

                                                    
                            # else:
                            #     info = {
                            #         "success": False,
                            #         "msg": "Insufficient balance to complete websms request"
                            #     }

                            #     return Response(info, status=status.HTTP_400_BAD_REQUEST)            



                else:
                        if message_type == "sms" or message_type == "SMS":
                            
                            if int(available_sms) >= len(senders_numbers):
        
                                url = env('SMS_URL')

                                payload = json.dumps({
                                        "privatekey": env('SMS_PRIVATE_KEY'),
                                        "publickey": env('SMS_PUBLIC_KEY'),
                                        "sender": env('SENDERS_ID'),
                                        "numbers": sending_numbers,
                                        "message": main_message
                                    })

                                headers = {
                                'Content-Type': 'application/json'
                                }

                                send_sms = requests.request("POST", url, headers=headers, data=payload).json()
                                # print(send_sms)

                                if send_sms['status'] == 1000:
                                    
                                    temp_sms.available_units -= len(senders_numbers)
                                    temp_sms.save()

                                    info = {
                                            "success": True,
                                            "msg": "Message(s) sent successfully"
                                        }

                                    return Response(info, status=status.HTTP_200_OK) 

                                else:
                                    info = {
                                            "success": False,
                                            "msg": "Server error"
                                        }

                                    return Response(info, status=status.HTTP_200_OK)                                 


                            else:
                                info = {
                                    "success": False,
                                    "msg": f"Insufficient balance. You can only send to {temp_sms.available_units} contact(s)"
                                }

                                return Response(info, status=status.HTTP_400_BAD_REQUEST)



                        elif "email" in message_type:

                            if int(available_email) >= len(sending_emails):
    
                                senders_mail = settings.EMAIL_HOST_USER
                                
                                email = EmailMessage(subject, main_message, senders_mail, sending_emails)

                                try:
                                    email.send()
                                    temp_email.available_units -= len(sending_emails)
                                    temp_email.save()

                                    info = {
                                            "success": True,
                                            "msg": "Message(s) sent successfully"
                                        }

                                    return Response(info, status=status.HTTP_200_OK) 

                                except: 
                                    print("Server error")
                                    pass

                                    info = {
                                            "success": False,
                                            "msg": "Server error"
                                        }

                                    return Response(info, status=status.HTTP_400_BAD_REQUEST)  

                            else:
                                info = {
                                    "success": False,
                                    "msg": f"Insufficient balance. You can only send to {temp_email.available_units} emails"
                                }

                                return Response(info, status=status.HTTP_400_BAD_REQUEST)



                        elif "audio" in message_type:

                            if int(available_audio) >= len(senders_numbers):
    
                                url = env('AUDIO_URL')

                                payload = json.dumps({
                                "id": env('SENDERS_ID'),
                                "caller_id": env('CALLERS_ID'),
                                "recipient": senders_numbers,
                                "media_url": audio_url,
                                "direction": env('DIRECTION')
                                })

                                headers = {
                                'Authorization': env('AUDIO_API_KEY'),
                                'Content-Type': 'application/json'
                                }

                                response = requests.request("POST", url, headers=headers, data=payload).json()
                                # print(response)


                                temp_audio.available_units -= len(senders_numbers)
                                temp_audio.save()


                                info = {
                                        "success": True,
                                        "msg": "Message(s) sent successfully"
                                    }

                                return Response(info, status=status.HTTP_200_OK)  
                            
                            else:
                                info = {
                                    "success": False,
                                    "msg": f"Insufficient balance. You can only send to {temp_audio.available_units} contacts"
                                }

                                return Response(info, status=status.HTTP_400_BAD_REQUEST)
                            


                        elif "websms" in message_type:

                            if int(available_websms) >= len(senders_numbers):
    
                                url = env('SMS_URL')

                                for i in senders_numbers:
                                    base_url = "https://postmaster.akwaabasoftware.com/"
                                    sid = f'{int(year)+added_post.id}'
                                    weblink = base_url + f'api/websms/{sid}/t={i}'

                                    sending_mail = main_message+"\n"+weblink

                                    payload = json.dumps({
                                    "privatekey": env('SMS_PRIVATE_KEY'),
                                    "publickey": env('SMS_PUBLIC_KEY'),
                                    "sender": env('SENDERS_ID'),
                                    "numbers": i,
                                    "message": sending_mail
                                    })

                                    headers = {
                                    'Content-Type': 'application/json'
                                    }

                                    send_sms = requests.request("POST", url, headers=headers, data=payload).json()
                                    if send_sms['status'] == 1000:
                                        temp_websms.available_units -= 1
                                        temp_websms.save()

                                info = {
                                        "success": True,
                                        "msg": "Message(s) sent successfully"
                                    }

                                return Response(info, status=status.HTTP_200_OK)             
                            else:
                                info = {
                                    "success": False,
                                    "msg": "Insufficient balance. You can only send to {temp_websms.available_units} contacts"
                                }

                                return Response(info, status=status.HTTP_400_BAD_REQUEST)  

        else:
            return Response(new_post.errors, status=status.HTTP_400_BAD_REQUEST)  




def viewWebmail(request, **kwargs):

    template_name = 'postman/view-webmail.html'

    string = kwargs.get('message_id')

    name = [i for i in string]

    stake = []
    stake.append(name[4])
    stake.append(name[5])
    stake.append(name[6])
    stake.append(name[7])

    num = ''.join(stake)

    pk = int(num)

    contact = kwargs.get('contact')

    mails = Post.objects.all()
    mail = get_object_or_404(Post, pk=pk)


    return render(request, template_name, {'mail': mail })





class ViewServiceTypes(APIView):
    
    def get(self, request):
        all_heroes = ServiceTypes.objects.all()
        heroes = ServiceTypesSerializer(all_heroes, many=True)

        info = {
            "count" : len(ServiceTypes.objects.all()),
            "data": heroes.data
        }
        
        return Response(info)
