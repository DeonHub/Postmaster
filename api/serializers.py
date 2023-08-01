from django.forms import ValidationError
from rest_framework import serializers
from .models import *
from postman.models import *


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    role = serializers.CharField()

    def validate_email(self, value):
        if len(value) < 5:
            raise ValidationError("No Jokes please")
        return value 
    
    def validate_password(self, value):
        if value == "":
            raise ValidationError("No Jokes please")
        return value 

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    client_id = serializers.CharField()
    branch = serializers.CharField()

    def validate_email(self, value):
        if len(value) < 5:
            raise ValidationError("No Jokes please")
        return value 
    
    def validate_password(self, value):
        if value == "":
            raise ValidationError("No Jokes please")
        return value 


class GroupSerializer(serializers.Serializer):
    # token = serializers.CharField()
    client_id = serializers.CharField()
    branch = serializers.CharField()
    group_name = serializers.CharField()
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise ValidationError("File shoulde be CSV")
        return value 



class ContactGroupSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = ContactGroups
        fields = ('group_name')





class ContactsSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Post
        fields = ('group_name', 'firstname', 'othername', 'email', 'contact' )


class PostsSerializer(serializers.ModelSerializer):
    
        class Meta():
            model = Post
            fields = '__all__'
            # fields = ('message', 'file', 'overtime_file', 'overtime_message', 'work_status')





class PostSerializer(serializers.Serializer):
    message_type = serializers.CharField()
    client_id = serializers.CharField()
    branch = serializers.CharField()
    description = serializers.CharField(required=False)                         
    description_type = serializers.CharField(required=False)
    schedule = serializers.BooleanField()
    schedule_date = serializers.DateField(required=False)
    schedule_time = serializers.TimeField(required=False)

    personalize = serializers.BooleanField(required=False)

    contacts = serializers.CharField(required=False)
    emails = serializers.CharField(required=False)

    contact_group = serializers.CharField(required=False)

    recurring = serializers.BooleanField()
    recurring_period = serializers.CharField(required=False)

    subject = serializers.CharField(required=False)
    main_message = serializers.CharField(required=False)

    draft = serializers.BooleanField(required=False)
    
    web_message = serializers.CharField(required=False)
    image_url = serializers.CharField(required=False)
    file = serializers.CharField(required=False)
    audio_url = serializers.CharField(required=False)


    # def get_validation_exclusions(self):
    #     exclusions = super(CommentSerializer, self).get_validation_exclusions()
    #     return exclusions + ['image_url', 'file', 'audio_url', 'schedule_date', 'schedule_time', 'contact_group', 'recurring_period', 'web_message','description', 'description_type']

    def validate(self, data):
        data_dict = dict(data)
        data_keys = data.keys()
        message_type = data_dict.get('message_type')
        schedule = data_dict.get('schedule')
        recurring = data_dict.get('recurring')
        description = data_dict.get('description')

        if message_type == "email" or "Email":
            if 'emails' not in data_keys:
                raise ValidationError("Field 'emails' are required for email messages")

            if 'main_message' not in data_keys:
                raise ValidationError("Field 'main_message' is required for Email messages")

            if 'personalize' in data_keys:
                raise ValidationError("Email messages cannot be personalized")

            if 'subject' not in data_keys:
                raise ValidationError("Field 'subject' is required for the email")


        if message_type == "sms" or "SMS": 
            if 'contacts' not in data_keys:
                raise ValidationError("Field 'contacts' are required for SMS messages")

            if 'main_message' not in data_keys:
                raise ValidationError("Field 'main_message' is required for SMS messages")


        if message_type == "audio" or "Audio":
            if 'audio_url' not in data_keys:
                raise ValidationError("Field 'audio_url' is required to send audio")

            if 'contacts' not in data_keys:
                raise ValidationError("Field 'contacts' are required for audio messages")    



        if message_type == "websms" or "WebSMS":
            if 'web_message' not in data_keys:
                raise ValidationError("Field 'web_message' is required to WebSMS messages")

            if 'contacts' not in data_keys:
                raise ValidationError("Field 'contacts' are required for WebSMS messages") 

            if 'main_message' not in data_keys:
                raise ValidationError("Field 'main_message' is required for WebSMS messages")
       




        if recurring == "True":
            if 'recurring_period' not in data_keys:
                raise ValidationError("Recurring period is required for recurring messages")


        if schedule == "True":
            if 'schedule_date' not in data_keys:
                raise ValidationError("Schedule date is required for scheduled message ('YY-MM-DD') ")

            if 'schedule_time' not in data_keys:
                raise ValidationError("Schedule time is required for scheduled message ('H:M')")

        return data    
               



class TopUpSerializer(serializers.Serializer):
    client_id = serializers.CharField()
    service_type = serializers.CharField()
    branch = serializers.CharField()
    amount_paid = serializers.FloatField()

    def validate_service_type(self, value):
        if value == False:
            raise ValidationError("You need to add service type")
        return value   


class AddCreditSerializer(serializers.Serializer):
    client_id = serializers.CharField()
    order_id = serializers.CharField()
    service_type = serializers.CharField()
    branch = serializers.CharField()


    def validate_client_id(self, value):
        if value == "False":
            raise ValidationError("No jokes please")
        return value   





class CreditsSerializer(serializers.Serializer):
    client_id = serializers.CharField()
    branch = serializers.CharField()

    def validate_branch(self, value):
        if value == False:
            raise ValidationError("Branch is required")
        return value   



class PurchaseSerializer(serializers.Serializer):
    client_id = serializers.CharField()

    def validate_client_id(self, value):
        if value == False:
            raise ValidationError("Client id is required")
        return value   



class PurchaseHistorySerializer(serializers.ModelSerializer):

    class Meta():
        model = TopUps
        fields = ('service_type', 'branch', 'amount_paid', 'date_created')




class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, value):
        if value == "":
            raise ValidationError("This field is required")
        return value        




class OutBoxSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Post
        fields = '__all__'
        # fields = ('message', 'file', 'overtime_file', 'overtime_message', 'work_status')






class ServiceTypesSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = ServiceTypes
        fields = '__all__'





# class CommentSerializer(serializers.Serializer):
#     rating = serializers.CharField(required=False)
#     remarks = serializers.CharField(required=False)

#     def get_validation_exclusions(self):
#         exclusions = super(CommentSerializer, self).get_validation_exclusions()
#         return exclusions + ['rating']


# All assigned duties
# class AssignedDutiesSerializer(serializers.ModelSerializer):

#     class Meta():
#         model = AssignedDutyActivities
#         fields = '__all__'
#         # fields = ('message', 'file', 'overtime_file', 'overtime_message', 'work_status')

