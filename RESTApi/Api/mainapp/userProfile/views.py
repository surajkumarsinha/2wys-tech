from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from django.contrib.auth.models import User
from ..authentication.models import User
from .serializers import ChangePasswordSerializer
from rest_framework import generics
# Create your views here.

Account = get_user_model()


class LoadProfileView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @staticmethod
    def post(request):
        user_id = request.data['EmailId']
        user = Account.objects.filter(EmailId=user_id).first()
        response = Response()
        response.data = {
            'FullName': user.FullName,
            'MobileNumber': user.MobileNumber
        }
        return response


class EditProfileView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @staticmethod
    def post(request):
        data = request.data
        if data['FullName'] is None or data['MobileNumber'] is None:
            raise Exception('The fields cannot be empty')

        user_id = request.COOKIES.get('id')
        user = Account.objects.filter(id=user_id).update(FullName=data['FullName'], MobileNumber=data['MobileNumber'])

        response = Response()
        response.data = user
        return response


class ChangePasswordView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @staticmethod
    def post(request):
        if User.objects.filter(EmailId = request.data['EmailId']):
            user = User.objects.get(EmailId = request.data['EmailId'])
        else:
            return Response( status=status.HTTP_400_BAD_REQUEST)   

        serializer = ChangePasswordSerializer(data = {
            'old_password': request.data['old_password'], 'new_password': request.data['new_password']
            })

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserDetailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @staticmethod
    def post(request):
        email = request.data['EmailId']
        if not User.objects.filter(EmailId = email):
            return Response("No such Email", status = status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(EmailId = email)[0]
        response = Response()
        response.data = {
            'FullName': user.FullName,
            'MobileNumber': user.MobileNumber, 
        }
        return response
