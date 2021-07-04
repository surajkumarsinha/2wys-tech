import json
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from ..authentication.models import User
from .models import UserSign, UserSignText, UserSignImage
from .serializers import CreateSignSerializer, CreateSignTextSerialzer, CreateSignImageSerialzer
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.core import serializers


class CreateSignView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    parser_class = (FileUploadParser,)
    parser_classes = (FormParser, MultiPartParser,)

    serializer_class1 = CreateSignSerializer
    serializer_class2 = CreateSignTextSerialzer
    serializer_class3 = CreateSignImageSerialzer
    
    
    def post(self, request):
        
        user = User.objects.get(EmailId = request.data['EmailId'])
        pos = request.data['SignPosition']
        loc = request.data['SignPage']
        f_name = request.data['FriendlyName']
        signtype = request.data['SignType']

        ser1 = self.serializer_class1(
            data = {
                'FriendlyName':f_name,
                'SignPage': loc,
                'SignPosition': pos
            })
        
        if ser1.is_valid():
            # with transaction.atomic():
            sign = ser1.save()
        else:
            return Response("Invalid Fields for ser1", status=status.HTTP_400_BAD_REQUEST)


        if signtype == 'Text':
            ser2 = self.serializer_class2(data = {
                'User':user.id,
                'Sign':sign.pk,
                'VisText': request.data['VisText']
            })

            if ser2.is_valid():
                with transaction.atomic():
                    ser2.save()
            else:
                return Response("Invalid ser2", status=status.HTTP_400_BAD_REQUEST)
        
        else:
            ser3 = self.serializer_class3(data = {
                'User':user.id,
                'Sign':sign.pk,
                'VisImage': request.data['Image']
            })

            if ser3.is_valid():
                with transaction.atomic():
                    ser3.save()

        return Response(ser1.data)
        

class DisplaySignView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):

        email = request.data['EmailId']

        if User.objects.filter(EmailId = email):
            user = User.objects.get(EmailId = email)
        else:
            Reponse("This is not a user", status=status.HTTP_400_BAD_REQUEST)

        # if UserSign.objects.filter(User = user.id).filter(FriendlyName = request.data['FriendlyName']):
        #     return Response("Signature already exists")

        signtext = UserSignText.objects.filter(User = user.id)
        signImage = UserSignImage.objects.filter(User = user.id)

        signtext = list(signtext)
        signImage = list(signImage)

        arr = []
        for q in signtext:
            base_sign = UserSign.objects.get(pk = q.Sign.pk) 
            dic = {
                'FriendlyName': base_sign.FriendlyName,
                'SignPage': base_sign.SignPage,
                'SignPosition': base_sign.SignPosition,
                'Text': q.VisText,
                'Type': "Text"
            }
            arr.append(dic)

        for q in signImage:
            base_sign = UserSign.objects.get(pk = q.Sign.pk) 
            dic = {
                'FriendlyName': base_sign.FriendlyName,
                'SignPage': base_sign.SignPage,
                'SignPosition': base_sign.SignPosition,
                'Image': str(q.VisImage),
                'Type': "Image"
            }
            arr.append(dic)

        response = Response()
        response.data = {"result" : arr}
        return response
        

class GetSignView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):

        response = Response()
        usersign = UserSign.objects.get(FriendlyName = request.data['FriendlyName'])
        if UserSignText.objects.filter(Sign= usersign.id):
            dic = {
                "sign_id": usersign.pk,
                "FriendlyName" : request.data['FriendlyName'],
                "SignPosition" : usersign.SignPosition,
                "SignPage" : usersign.SignPage,
                "VisText" : UserSignText.objects.get(Sign = usersign.id).VisText
            }

        elif UserSignImage.objects.filter(Sign = usersign.id):
            dic = {
                "sign_id": usersign.pk,
                "FriendlyName" : request.data['FriendlyName'],
                "SignPosition" : usersign.SignPosition,
                "SignPage" : usersign.SignPage,
                "VisText" : UserSignImage.objects.get(Sign = usersign.id).VisImage
            }

        response.data = dic
        return response

class EditSignView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):

        # get the details of the sign
        email = request.data['EmailId']
        F_Name = request.data['FriendlyName']
        signpos = request.data['SignPosition']
        signpage = request.data['SignPage']

        user = User.objects.get(EmailId = email)
        if not UserSign.objects.filter(FriendlyName = F_Name):
            return Response("The Signature Doesn't exist. Create one", status=status.HTTP_400_BAD_REQUEST)

        usersign = UserSign.objects.filter(FriendlyName = F_Name)
        usersign.update(SignPosition = signpos, SignPage = signpage)
        
        # If it is an text sign
        if UserSignText.objects.filter(Sign = usersign[0].id):
            UserSignText.objects.filter(Sign = usersign[0].id).update(VisText = request.data['VisText'])

        # If sign is an image
        elif UserSignImage.objects.filter(Sign = usersign.id):
            UserSignImage.objects.filter(Sign = usersign[0].id).update(VisImage = request.data['VisImage'])

        return Response("The Sign has been updated")
        


class DeleteSignView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):

        email = request.data['EmailId']
        F_Name = request.data['FriendlyName']

        sign = UserSign.objects.filter(FriendlyName = F_Name)
        sign.delete()

        return Response("Sign deleted")