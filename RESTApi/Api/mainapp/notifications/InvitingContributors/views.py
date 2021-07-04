from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes , force_text
from django.db import transaction
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlencode

from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView

from ...utils.notif import default_token_generator, account_activation_token, decode
from ...authentication.serializers import UseAccSerializer
from ...authentication.models import User, Account, User_Account

# from ..index import SendMail
from ...tasks import SendMail


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def ContributorConfirm(request, uidb64 , token):
    ctx = {}
    if request.method == 'GET':
        try:
            user, account = decode(uidb64)

        except(TypeError, ValueError, OverflowError):
            user = None

        if user is not None and account is not None and default_token_generator.check_token(user, account, token):
            
            # If user exists already then he will just be joined
            
            if User.objects.filter(EmailId=user):
            
                user = User.objects.get(EmailId=user)
                
                if not User_Account.objects.filter(acc = account).filter(user=user.id):    
                    ser3 = UseAccSerializer(data={'user': user.id, 'acc': account, 'is_owner': False})
                    if ser3.is_valid():
                        with transaction.atomic():
                            ser3.save()
                    # Return to a "Thank You For joining" Template  
                    ctx = {"message": "Thank you for joining"}
                    return render(request, 'Inval_Thank.html', ctx) 

                else :
                    # return HttpResponse("User is already joined")
                    return redirect('/api/Acutes/SignIn/')

            
            # If he doesn't exist then he will be redirected to the signup page with fields off
            else: 
                base_url = reverse('SignUp')
                query_string = urlencode({'uid':uidb64, 'token':token})
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)
            

        else:
            ctx = {"message": "This link has expired/invalid"}
            return render(request, 'Inval_Thank.html', ctx)

  
#  Testing Zone #

def InviteContributorss(email, dic_bod, current_site):

    dic = {}
    account = Account.objects.filter(AccountName = dic_bod['Account'])
    users = dic_bod['Users_Invited'] # will be a list of users
    sender = email   
    
    sender_name = User.objects.get(EmailId=sender).FullName

    if account :
        account = account[0]
        from_email = settings.EMAIL_HOST_USER
        
        template = '2WYS_Invitation_Mail.html'
        
        for user in users:
            dic ={   
                    'subject': "Invitation to contribute",
                    'message': "Inviting all the contributors",
                    'domain' : current_site.domain,
                    'uid' : urlsafe_base64_encode(force_bytes("EmailId:"+str(user)+"<#>account:"+str(account.pk))),
                    'token': default_token_generator.make_token(account.pk, user),
                    'account': account.AccountName,
                    'FullName': sender_name,
                    'Sender': sender,
                    'attach_filename': None
                }
            print(current_site.domain)
            # SendMail(from_email, [user], dic, template)
        # SendMail.delay(from_email, to_list, dic, template)
