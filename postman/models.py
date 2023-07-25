from django.db import models


# Create your models here.
class Post(models.Model):
    message_id = models.CharField(max_length= 100, null=True)
    client_id = models.CharField(max_length= 100, null=True, default="1")
    branch = models.CharField(max_length= 100, null=True, default="Main Branch")
    schedule = models.BooleanField(default=False)
    schedule_date = models.DateField(blank=True, null=True)
    schedule_time = models.TimeField(blank=True, null=True)
    personalize = models.BooleanField(default=False)
    contacts= models.CharField(max_length= 5000, null=True)
    description= models.CharField(max_length= 100, null=True)
    description_type= models.CharField(max_length= 100, null=True)
    contact_group = models.CharField(max_length=150, null=True)
    total_contacts = models.IntegerField(null=True, default=0)
    recurring = models.BooleanField(default=False)
    recurring_period = models.CharField(max_length= 150, null=True, blank=True, default="None")
    message_type = models.CharField(max_length= 150, null=True)
    subject = models.CharField(max_length= 150, null=True)
    main_message = models.CharField(max_length= 1000, null=True)
    total_characters = models.IntegerField(null=True, default=0)
    draft = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    web_message = models.CharField(max_length= 1000, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='image-uploads/', default='')
    file = models.FileField(blank=True, null=True, upload_to='file-uploads/', default='')
    audio_file = models.FileField(blank=True, null=True, upload_to='audio-uploads/', default='')
    sent_by =  models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.message_type} sent on {self.date_created}'



class ClientEmails(models.Model):
    client_id = models.CharField(max_length=100, null=True)
    branch = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True) 
    password = models.CharField(max_length=15, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client_id} created on {self.date_created}'    


class ContactGroups(models.Model):
    group_name = models.CharField(max_length=100, null=True)
    firstname = models.CharField(max_length=100, null=True)
    othername = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True) 
    contact = models.CharField(max_length=15, null=True)
    sent_by=models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.group_name} created on {self.date_created}'



# class AssignedDutyActivities(models.Model):
#     branch = models.CharField(max_length= 100, null=True)
#     member_category = models.CharField(max_length= 100, null=True)
#     group = models.CharField(max_length= 100, null=True)
#     subgroup = models.CharField(max_length= 100, null=True)
#     member = models.CharField(max_length= 100, null=True)
#     message = models.CharField(max_length= 500, null=True)
#     file = models.FileField(blank=True, null=True, upload_to='file-uploads/', default='')
#     start_date = models.DateField(blank=True, null=True)
#     end_date = models.DateField(blank=True, null=True)
#     start_time = models.TimeField(blank=True, null=True)
#     end_time = models.TimeField(blank=True, null=True)
#     duty_subject = models.CharField(max_length= 100, null=True)
#     new_subject = models.CharField(max_length= 100, null=True)

#     report_status = models.CharField(max_length= 100, null=True, default="Not submitted")

#     report_message = models.CharField(max_length= 500, null=True, default="No message")
#     report_file = models.FileField(blank=True, null=True, upload_to='file-uploads/', default='')
#     overtime_message = models.CharField(max_length= 500, null=True, default="No message")
#     overtime_subject = models.CharField(max_length= 500, null=True, default="No subject")
#     overtime_file = models.FileField(blank=True, null=True, upload_to='file-uploads/', default='')
#     percentage_done = models.IntegerField(null=True, default=0)

#     work_status = models.CharField(max_length= 500, null=True, default="Undone")
    
#     rating = models.CharField(max_length= 500, null=True, default="Unrated")
#     remarks = models.CharField(max_length= 500, null=True, default="No remarks")

#     extra = models.BooleanField(default=False)

#     assigned = models.BooleanField(default=False)
#     self_assigned = models.BooleanField(default=False)
#     reassigned = models.BooleanField(default=False)

#     reassigned_to = models.CharField(max_length= 500, null=True, default="No one")
#     reassigned_from = models.CharField(max_length= 500, null=True, default="No one")

#     date_created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.member}, {self.duty_subject}'



class ServiceTypes(models.Model):
    service_type = models.CharField(max_length= 100, null=True)
    unit_amount_usd = models.FloatField(null=True, default=0)
    unit_amount_ghs = models.FloatField(null=True, default=0)
    date_created = models.DateField(auto_now_add= True)

    def __str__(self):
        return f"{self.service_type} at USD {self.unit_amount_usd}/ GHS {self.unit_amount_ghs}"


class TopUps(models.Model):
    client_id = models.CharField(max_length= 100, null=True)
    service_type = models.CharField(max_length= 100, null=True)
    account_type = models.CharField(max_length= 100, null=True)
    branch = models.CharField(max_length= 100, null=True)
    order_id = models.CharField(max_length= 100, null=True)
    amount_paid = models.FloatField(null=True, default=0)
    confirmed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add= True)

    def __str__(self):
        return f"{self.service_type} for Client {self.client_id}, ({self.branch})"


class Credits(models.Model):
    client_id = models.CharField(max_length= 100, null=True)
    service_type = models.CharField(max_length= 100, null=True)
    branch = models.CharField(max_length= 100, null=True)
    available_units = models.IntegerField(null=True, default=0)
    date_created = models.DateField(auto_now_add= True)

    def __str__(self):
        return f"{self.service_type} for Client {self.client_id}, ({self.branch})"



class ActivityLog(models.Model):
    user = models.CharField(max_length= 100, null=True)
    action = models.CharField(max_length= 100, null=True)
    date_created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.user} {self.action}"