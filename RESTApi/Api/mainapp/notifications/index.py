from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, serializers
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.contrib.auth import views as auth_views
from ..authentication.models import User
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status

# Notification functions
from .PasswordReset.views import PasswordResetter
from .InvitingContributors.views import InviteContributorss
from .ShareFiles.views import ShareFiles
"""
# Note : 'Forgot password?'-> redirect to enter email page -> if email is in db -> send email with a link 
                                                                            #   -> redirect to the signup page            
"""
# Dictionary for Reason of Notif


Type = [
    {
        'Name':'ChangePassword',
        'Subject': 'Please Enter your Email Id',
    }, 

    {
        'Name':'InviteContributors',
        'Subject': 'Please enter Email of the contributor',
    }
]

# List for method of Notif
Method = {
            1:'Mail', 
            2:'SMS',
        }

@authentication_classes([])
@permission_classes([AllowAny])
class NotificationView(APIView):

    @staticmethod
    def post(request):

        # The Request body
        NotifType = request.data['NotificationType']
        NotifMethod = request.data['NotificationMethod']
        Sender_mail = request.data['EmailId']
        dict_body = request.data['dic']

        current_site = get_current_site(request)

        # If the sender even exists
        if User.objects.filter(EmailId=Sender_mail):
        
            if NotifType == 'ChangePassword' and NotifMethod == 'Mail':
                PasswordResetter(Sender_mail, dict_body, current_site)
                message = "Mail has been sent"

            elif NotifType == 'InviteContributors' and NotifMethod == 'Mail':
                InviteContributorss(Sender_mail, dict_body, current_site)
                message = "Contributer has been sent the invitation"

            elif NotifType == 'ShareFiles' and NotifMethod == 'Mail':
                ShareFiles(Sender_mail, dict_body)
                message = "The files have been shared"
            
        else:
             message = "The sender Email is invalid. Please Check"
        
        response = Response()
        response.data = {"message": message}
        return response



# URL = 'https://www.sms4inida.com/api/v1/sendcampaign'
# response = SendMessage(
#         URL, 
#         'provided-api-key', 
#         'provided-secret-key', 
#         'stage/prod', 
#         'valid-to-mobile', 
#         'active-sender-id',
#         'text-message'
#     )