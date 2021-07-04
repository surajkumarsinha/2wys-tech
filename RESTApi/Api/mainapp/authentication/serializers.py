import re
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import serializers
from .models import User, Account, User_Account
# from rest_framework_recaptcha.fields import ReCaptchaField

VALID_EMAIL = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


# class MyReCaptchaField(ReCaptchaField):
#     default_error_messages = {
#         "invalid-input-response": "reCAPTCHA token is invalid.",
#     }


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["AccountName"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['EmailId', 'FullName', 'MobileNumber', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        account = User.objects.create_user(**validated_data)
        return account


# For storing the combined pk for both account as well as user
class UseAccSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Account
        fields = ['user', 'acc', 'is_owner']


class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['EmailId', 'password']
        extra_kwargs = {"password": {"write_only": True}, "EmailId": {"validators": []}}

    verify_email = None

    def validate_email(self, EmailId):
        if not User.objects.filter(EmailId=EmailId).exists():
            raise ValidationError('No Such Email exists')
        if not EmailId:
            raise ValidationError('This is a required field')
        if not re.match(VALID_EMAIL, EmailId):
            raise ValidationError('Invalid Email passed')
        self.verify_email = EmailId
        return EmailId

    def validate_password(self, password):
        if not password:
            raise ValidationError('This is a required filed')
        try:
            user = User.objects.get(EmailId=self.verify_email)
            if not user.check_password(password):
                raise ValidationError("Invalid Password")
        except ObjectDoesNotExist:
            # Already raised in validate_email, no need to raise again
            pass
        return password

    def validate(self, data):
        EmailId = data["EmailId"]
        password = data["password"]

        self.user = authenticate(
            request=self.context["request"], EmailId=EmailId, password=password
        )
        if not self.user:
            # raise ValidationError("Invalid username or password")
            self.validate_email(EmailId)
            self.validate_password(password)

        return data

    def save(self):
        return self.user


# --------------- Reference Testing Section ------------- #

"""
class AccountCreationSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ["AccountName", ]

class SignUpSerializer2(ModelSerializer):
    AccountData = AccountCreationSerializer(many=True, source="AccountName")

    class Meta:
        model = User
        fields = ['email', 'AccountData', 'FullName', 'MobileNumber', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def validate(self, attrs):
        attrs = super(SignUpSerializer2, self).validate(attrs=attrs)
        attrs.update({"AccountData": self.initial_data.get("AccountData")})
        return attrs

    def create(self, validated_data):
        AccountName_data = validated_data.pop('AccountData')
        userAcc = User.objects.create_user(**validated_data)
        acc = Account.objects.create(AccountName=AccountName_data)
        if acc:
            userAcc.AccountName.add(acc)

        return userAcc

    def update(self, instance, validated_data):
        print("updating")
        AccountName_data = validated_data.pop('AccountData')
        accounts = instance.AccountData.all()
        # accounts = list(accounts)
        instance.email = validated_data.get('email', instance.email)
        instance.FullName = validated_data.get('FullName', instance.FullName)
        instance.MobileNumber = validated_data.get('MobileNumber', instance.MobileNumber)
        instance.save()
        acc = Account.objects.create(AccountName=AccountName_data)
        accounts.append(acc)
        instance.AccountName.add(accounts)
        # for acc_data in AccountName_data:

        # print(instance)
        # for account_data in AccountName_data:
        #     account = AccountName_data.pop('AccountData')

"""
# ------------------------Ends------------------------- #
