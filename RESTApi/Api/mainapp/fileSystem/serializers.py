from rest_framework.exceptions import ValidationError
from .models import FilesModel
from rest_framework import serializers
from ..authentication.models import User_Account


class FileUploadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = FilesModel
        fields = ['id','File', 'Account', 'User', 'IsSigned', 'Date', 'DateTime']

    @staticmethod
    def validate_file(file):
        st = str(file).split('.')
        # print(st[1])
        if not str(file).endswith('.pdf') and not str(file).endswith('.PDF'):
            raise ValidationError("The File is not a pdf document")

    @staticmethod
    def validate_user_acc(user, acc):
        if not User_Account.objects.filter(user=user, acc=acc):
            raise ValidationError("No User in this account")

    def validate(self, data):
        self.validate_file(data['File'])
        self.validate_user_acc(data['User'], data['Account'])
        return data


class FileDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilesModel
        fields = ['File', 'Account', 'User']
