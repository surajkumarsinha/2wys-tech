from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes , force_text
from django.db import transaction
from django.core.mail import EmailMessage
from django.conf import settings

from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView

from ...utils.notif import default_token_generator, account_activation_token
from ...authentication.serializers import UseAccSerializer
from ...authentication.models import User, Account, User_Account

# from ..index import SendMail
from ...tasks import SendMail

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def PasswordReset(request):

    email = request.data['EmailId']
    email_user = User.objects.filter(EmailId=email)

    if len(email_user) != 0:
        user = email_user[0]
        from_email = settings.EMAIL_HOST_USER
        to_list = [email]
        current_site = get_current_site(request)
        
        template = 'EmailBodySent.html'
        dic ={
                'subject': "Password Reset",
                'message': "Here is the link for password change",
                'user' : user,
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'account': None,
                'attach_filename': None
            }

        SendMail(from_email, to_list, dic, template)
        # SendMail.delay(from_email, to_list, dic, template)
        txt = "Mail Sent"
        # url_render = '/api/Acutes/Reset/password_reset_done/'
        return Response(status = status.HTTP_200_OK)
        # return url_render
    
    else:
    
        txt = 'There is no such user'

    return HttpResponse(txt)



@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def PasswordResetConfirm(request, uidb64 , token):
    
    if request.method == 'GET':
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            ctx = {"user": user.EmailId}
            
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            
            return render(request, 'PasswordReset.html', ctx)
            
        else:
            ctx = {"message": "This link has expired/invalid"}
            return render(request, 'Inval_Thank.html', ctx)
            

    if request.method == 'POST':
        password1 = request.data['password1']
        password2 = request.data['password2']

        if password1 == password2:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            user.set_password(password1)
            user.save()
            return redirect('/api/Acutes/Reset/password_reset_complete/')
            # return Response("Password Changed", status=status.HTTP_200_OK)
        else:
            message =  'Invalid Password Credentials'
            ctx = {
                    'message' : message,
            }
            return render(request, 'PasswordReset.html', ctx)



@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def PasswordResetDone(request):
    template = loader.get_template('PasswordMailSent.html')
    ctx = {}
    return HttpResponse(template.render(ctx,request))


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def PasswordResetComplete(request):
    if request.method == 'GET':
        ctx = {}
        return render(request, 'ResetComplete.html', ctx)




#  Testing Zone #


def PasswordResetter(email, dic_bod, current_site):

    # email = request.data['EmailId']
    email_user = User.objects.filter(EmailId=email)

    if len(email_user) != 0:
        user = email_user[0]
        from_email = settings.EMAIL_HOST_USER
        to_list = [email]
        
        
        template = 'EmailBodySent.html'
        dic ={
                'subject': "Password Reset",
                'message': "Here is the link for password change",
                'user' : user,
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'account': None
            }

        SendMail(from_email, to_list, dic, template)
        # SendMail.delay(from_email, to_list, dic, template)
        txt = "Mail Sent"
        
        # return Response(status = status.HTTP_200_OK)
        return redirect('/api/Acutes/Reset/password_reset_done/')
    
    # else:
    
    #     txt = 'There is no such user'

    # return HttpResponse(txt)
