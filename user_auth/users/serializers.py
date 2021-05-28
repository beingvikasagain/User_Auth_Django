from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from user_auth import settings
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail

from .models import *
from .functions import generate_confirmation_token, confirm_token, send_verification_email

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password':{'write_only':True}}
        
    def validate(self, data):
        for key in ['first_name', 'last_name', 'email', 'password']:
            if key not in data:
                raise serializers.ValidationError("missing one or more required keys ['first_name', 'last_name', 'email', 'password']")
        
        return data
    
    def save(self):
        user = User.objects.create_user(self.validated_data['first_name'], self.validated_data['last_name'],
                                        self.validated_data['email'], self.validated_data['password'])
        # sendConfirm(user)
        if not send_verification_email(user):
            return Response({'success': 'false', 'message': 'verification email failed'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        data={}
        data['message'] = 'verification email sent successfully'
        data['email'], data['first_name'], data['last_name'] = user.email, user.first_name, user.last_name
        return Response(data)