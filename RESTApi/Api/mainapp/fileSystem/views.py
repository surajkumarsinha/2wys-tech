import json
import os
from io import BufferedReader
import base64
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, serializers, mixins
from rest_framework.settings import api_settings
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from io import BytesIO, StringIO
from .serializers import FileUploadSerializer
from django.http import HttpResponse
from django.core import serializers
from django.conf import settings

from .models import FilesModel
from .mixins import MyPaginationMixin
from ..authentication.models import Account, User_Account, User
from ..utils.files import (
                            check_cred,
                            sign_filter,
                            date_filter,
                            user_filter,
                            create_zip,
                            check_dir_path
                        )
from ..utils.notif import zip_guid


@authentication_classes([])
@permission_classes([])
class FileUploadView(APIView):

    parser_class = (FileUploadParser,)
    parser_classes = (FormParser, MultiPartParser,)
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    @staticmethod
    def post(request):
        check_cred(request.data['EmailId'], request.data['Account'])

        user = User.objects.get(EmailId=request.data['EmailId'])
        account = Account.objects.get(AccountName=request.data['Account'])

        f = []
        for u in request.FILES.getlist('files'):

            f_name = "user_" + str(user.id) + "/unsigned/" +  str(u)
        
            IsSigned = False
            file_serializer = FileUploadSerializer(data={
                'File': u,
                'User': user.id,
                'Account': account.id,
                'IsSigned': IsSigned
            })

            if FilesModel.objects.filter(File=f_name):
                raise  ValidationError("The file already exists")
                

            if file_serializer.is_valid():
                file_serializer.save()
                f.append(file_serializer.data['File'])
                
        response = Response()
        response.data = {'Files' : f}
        return response

        

@authentication_classes([])
@permission_classes([])
class FileDownloadView(APIView):
    parser_class = (FileUploadParser,)

    @staticmethod
    def post(request):
        check_cred(request.data['EmailId'], request.data['Account'])

        user = User.objects.get(EmailId=request.data['EmailId'])
        account = Account.objects.get(AccountName=request.data['Account'])

        queryset = FilesModel.objects.filter(User=user.id,
                                             Account=account.id,
                                             pk__in=request.data['FileIds']
                                             )                                     
        if len(queryset) == 0:
            return Response("No such files", status=status.HTTP_400_BAD_REQUEST)

        if len(request.data['FileIds']) > 1:
            
            check_dir_path('media', 'zipfiles')
            zip_filename = create_zip(queryset, True, "2WYS_Downloads", user)

            response = Response()
            response.data = {
                "zip_path": zip_filename
            }
            return response

        else:
            qs_json = serializers.serialize('json', queryset)
            return HttpResponse(qs_json, content_type='application/json')


@authentication_classes([])
@permission_classes([]) 
class LoadGrid(APIView, MyPaginationMixin):
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    serializer_class = FileUploadSerializer
    queryset = FilesModel.objects.all()
    # page_size = 1
    # pagination_class.page_size = page_size
    
    def post(self, request):
        check_cred(request.data['EmailId'], request.data['Account'])

        user = User.objects.get(EmailId=request.data['EmailId'])
        account = Account.objects.get(AccountName=request.data['Account'])
        is_owner = User_Account.objects.get(user=user.id, acc=account.id).is_owner
        
        # if request.data['PageSize'] is not None:
        #     self.pagination_class.page_size = request.data['PageSize']
        # filter by the user if owner
        if is_owner:
            if request.data["UserFilter"] != 'All':
                queryData_user = user_filter(account.id, request.data["UserFilter"])
            else:
                queryData_user = FilesModel.objects.filter(User=user.id, Account=account.id)
        else:
            queryData_user = FilesModel.objects.filter(User=user.id, Account=account.id)

        # filter by sign nature
        queryset_type_sign = sign_filter(queryData_user, request.data['TypeFilter'])

        # filter by range of time
        queryset_type_date = date_filter(queryset_type_sign, request.data["StartDate"], request.data["EndDate"])
        
        page = self.paginate_queryset(queryset_type_date)
        if len(page) == 0:
            response = Response()
            response.data = {
                "count":0,
                "next": None,
                "prev": None,
                "results":[]
            }
            return response

        if page is not None:
            serializer = self.serializer_class(page, many=True)

            for obj in serializer.data:
                acc_id = obj['Account']
                user_id = obj['User']
                obj['User'] = User.objects.get(pk=user_id).FullName
                obj['Account'] = Account.objects.get(pk=acc_id).AccountName
            
            # return Response(serializer.data[0])
            return self.get_paginated_response(serializer.data)

        return Response("Invalid Params", status = status.HTTP_400_BAD_REQUEST)
        

@authentication_classes([])
@permission_classes([])
class load_account_users(APIView):
    @staticmethod
    def post(request):
        check_cred(request.data['EmailId'], request.data['Account'])

        user = User.objects.get(EmailId=request.data['EmailId'])
        account = Account.objects.get(AccountName=request.data['Account'])
        if User_Account.objects.filter(user=user.id, acc=account.id):
            is_owner = User_Account.objects.get(user=user.id, acc=account.id).is_owner
        else:
            raise ValidationError("Not the owner")

        val = []

        if is_owner:
            queryset = User_Account.objects.filter(acc=account.id)
            users_acc = list(queryset)

            for user_acc in users_acc:
                val.append(user_acc.user.EmailId)

        response = HttpResponse()
        response.data = {
            "Users": val
        }
        return response



@authentication_classes([])
@permission_classes([])
class GetSignedFile(APIView):
    serializer_class = FileUploadSerializer

    def post(self, request):
        data = request.data['Data']
        file_id = request.data['FileID']
        isSigned = True
        file_data = FilesModel.objects.filter(pk=file_id)[0]
        # FilesModel.objects.filter(pk=file_id).update(IsSigned=False)
        user_id = file_data.User_id
        file_name = str(file_data.File)
        file_name_end = file_name.split('/')[2]
        check_dir_path('media/user_'+str(user_id), 'signed')
        
        path = 'media/user_' + str(user_id) + '/signed/'+ file_name_end
        with open(path, 'wb') as pdf:
            pdf.write(base64.b64decode(data))
    
        name = pdf.name.split('/', 1)
        FilesModel.objects.filter(pk=file_id).update(IsSigned = True, File = pdf.name.split('/', 1)[1])
        
        return Response("File has been signed")


#   Not in use anymore  #
@authentication_classes([])
@permission_classes([])   
class QuerysetConvert(APIView):
    
    @staticmethod
    def post(request):
        q = request.data["results"]
        for i in q:
            temp = i['User']
            i['User'] = User.objects.get(pk=temp).FullName

        qs_json = json.dumps(q)
        return HttpResponse(qs_json, content_type='application/json')