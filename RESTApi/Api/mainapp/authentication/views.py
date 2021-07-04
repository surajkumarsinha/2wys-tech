from django.db import transaction
from django.http import HttpResponse
from rest_framework.exceptions import ValidationError
# from rest_framework.throttling import UserRateThrottle
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .serializers import (
    SignInSerializer,
    AccountSerializer,
    UserSerializer,
    UseAccSerializer
)
# from rest_framework.authentication import SafeJWTAuthentication
# from .authentication import SafeJWTAuthentication

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from ..utils.auth import (
    make_response,
    login_user,
    access_token_refresh
)

# from .prevent import UserLoginRateThrottle
from .models import User, User_Account, Account
from django.contrib.auth import get_user_model
from ..utils.notif import default_token_generator, decode

@authentication_classes([])
@permission_classes([])
class SignUpView(APIView):
    serializer_class1 = UserSerializer
    serializer_class2 = AccountSerializer
    serializer_class3 = UseAccSerializer
   
   
    def post(self, request, *args, **kwargs):

        # If the user is Invited and User is not signed up
        if request.query_params : 
            token = request.query_params['token']
            uid = request.query_params['uid']
            user, account_id = decode(uid)
            token_flag = default_token_generator.check_token(user, account_id, token)
            
            if token_flag and user and account_id:
                CreateAccount = False
                is_owner = False
                request.data['AccountName'] = Account.objects.get(pk = account_id).AccountName 
                request.data['EmailId'] = user
             
            else:
                return HttpResponse("ERROR 404 Invalid Credentials")
       
        else:
            CreateAccount = True
            is_owner = True
    
        user_found = False if not User.objects.filter(EmailId=request.data['EmailId']) else True
        is_owner = False

        # Opening a new account
        if CreateAccount:
            is_owner = True
            # To check if the account already exists. Raise Exception if it is present
            if Account.objects.filter(AccountName=request.data['AccountName']):
                raise Exception("This Account Already Exists")

            if not user_found:
                ser1 = self.serializer_class1(data=request.data)
                if ser1.is_valid():
                    with transaction.atomic():
                        ser1.save()
                else:
                    raise ValidationError("The User fields are invalid")

            ser2 = self.serializer_class2(data={'AccountName': request.data['AccountName']})
            if ser2.is_valid():
                with transaction.atomic():
                    ser2.save()
            else:
                raise ValidationError("The Account fields are invalid")

        # joining account but user doesn't exist
        elif not User.objects.filter(EmailId=request.data['EmailId']):
            ser1 = self.serializer_class1(data=request.data)

            if ser1.is_valid():
                with transaction.atomic():
                    ser1.save()
            else:
                raise ValidationError("The fields are invalid")

        
        user = User.objects.get(EmailId=request.data['EmailId'])
        if Account.objects.filter(AccountName=request.data['AccountName']):
            acc = Account.objects.get(AccountName=request.data['AccountName'])
        else:
            raise ValidationError("You cannot attach to this Account")

        
        ser3 = self.serializer_class3(data={'user': user.id, 'acc': acc.id, 'is_owner': is_owner})
        if ser3.is_valid():
            with transaction.atomic():
                ser3.save()

        return Response(status=status.HTTP_200_OK)


@authentication_classes([])
class SignInView(APIView):
    # throttle_classes = (UserLoginRateThrottle,)
    serializer_class = SignInSerializer
    permission_classes = [AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        
        data = request.data
        serializer = self.serializer_class(
            data=data,
            context={"request": request}
        )

        if not serializer.is_valid():
            first_errors = {k: v[0] for k, v in serializer.errors.items()}
            return make_response(False, first_errors)

        user = serializer.save()
        tokenvals = login_user(request, user)
        response = Response()
        response.set_cookie(key='refreshtoken', value=tokenvals['refresh_token'], httponly=True, )
        response.set_cookie(key="accesstoken", value=tokenvals['access_token'], httponly=True, )
        # response.set_cookie(key="id", value=user.id)
        response.data = {
            'access_token': tokenvals['access_token'],
            'id': user.id,  # store it inside sessionStorage
            'EmailId': user.EmailId  # store it inside sessionStorage or LocalStorage

        }

        return response
        # return Response(status=status.HTTP_200_OK)

 
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])  
@csrf_protect
def token_refresh(request):
    data = access_token_refresh(request)
    response = Response()
    response.set_cookie(key="accesstoken", value=data['access_token'], httponly=True, )
    response.data = data
    return response


class SignOutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @method_decorator(csrf_protect)
    def post(self, request):

        response = Response()

        if request.COOKIES.get('refreshtoken'):
            response.delete_cookie('refreshtoken')

        if request.COOKIES.get('accesstoken'):
            response.delete_cookie('accesstoken')

        if request.COOKIES.get('csrftoken'):
            response.delete_cookie('csrftoken')

        if request.COOKIES.get('sessionid'):
            response.delete_cookie('sessionid')

        return response


class GetUserAccounts(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        if User.objects.filter(EmailId=request.data['EmailId']):
            user = User.objects.get(EmailId=request.data['EmailId'])
        else:
            return Response("User doesn't exist", status=status.HTTP_400_BAD_REQUEST)
        user_accounts = User_Account.objects.filter(user=user.id)
        user_accounts = list(user_accounts)
        val = []
        for user_account in user_accounts:
            val.append({'Account' :user_account.acc.AccountName})

        response = Response()
        response.data = {
            'result': val
        }
        return response

