import json
import os
import zipfile
from ...authentication.models import User
from ...fileSystem.models import FilesModel
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from ...tasks import SendMail
from django.conf import settings
from ...utils.files import create_zip, check_dir_path

@authentication_classes([])
@permission_classes([AllowAny])
def ShareFiles(email, dict_bod):

    # dic_bod will contain list of file ids
    users = dict_bod['Users_Invited'] # will be a list of users
    sender = email
    queryset = dict_bod['FileIds']
    from_email = settings.EMAIL_HOST_USER
    file_path = ""

    if len(queryset) > 1:
        check_dir_path('media', 'zipfiles')
        # push it into utils
        zip_filename = create_zip(queryset, False, "2WYS_Attachment", None)
        file_path = zip_filename

    else:
        fid = queryset[0]
        fname = FilesModel.objects.get(pk=str(fid)).File
        file_path = 'media/'+ str(fname)
        
    for user in users:
        template = 'ShareFiles.html'
        dic ={
                'subject': "Sharing Files",
                'message': "Here are the files shared with you",
                'account': None,
                'sender': sender,
                'attach_filename': file_path
            }
        SendMail(from_email, [user], dic, template)