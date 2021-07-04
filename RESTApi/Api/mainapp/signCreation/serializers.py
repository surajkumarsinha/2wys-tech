from rest_framework import serializers
from ..authentication.models import User
from .models import UserSign, UserSignText, UserSignImage
from rest_framework.exceptions import ValidationError

class CreateSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSign 
        fields = '__all__'

        

class CreateSignTextSerialzer(serializers.ModelSerializer):
    class Meta:
        model = UserSignText 
        fields = ['User', 'Sign', 'VisText']


class CreateSignImageSerialzer(serializers.ModelSerializer):
    class Meta:
        model = UserSignImage 
        fields = ['User', 'Sign', 'VisImage']

