from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from datetime import datetime
from django.conf import settings
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36
from django.utils.encoding import force_bytes , force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from ..authentication.models import User, User_Account, Account

class AccountTokenGenerator:

    key_salt = "django.CreateToken.For.Inviting.Contributors"
    algorithm = None # include secret key
    secret = None # include hash algo

    def __init__(self):
        self.secret = self.secret or settings.SECRET_KEY
        
        # self.algorithm = self.algorithm or 'sha256'
        self.algorithm = self.algorithm or settings.DEFAULT_HASHING_ALGORITHM

    def make_token(self, account, user):

        return self._make_token_with_timestamp(user, account, self._num_seconds(self._now()))

    def check_token(self, user, account, token):

        if not (user and account and token):
            return False
        # Parse the token
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, account, ts), token):
            # RemovedInDjango40Warning: when the deprecation ends, replace
            # with:
            #   return False
            if not constant_time_compare(
                self._make_token_with_timestamp(user, account, ts, legacy=True),
                token,
            ):
                return False

        # Check the timestamp is within limit.
        if (self._num_seconds(self._now()) - ts) > settings.PASSWORD_RESET_TIMEOUT:
            return False

        return True

    def _make_token_with_timestamp(self, user, account, timestamp, legacy=False):

        ts_b36 = int_to_base36(timestamp)
        hash_string = salted_hmac(
            self.key_salt,
            self._make_hash_value(user, account, timestamp),
            secret=self.secret,
            algorithm='sha1' if legacy else self.algorithm,
        ).hexdigest()[::2]  # Limit to shorten the URL.
        return "%s-%s" % (ts_b36, hash_string)

    def _make_hash_value(self, user, account, timestamp):
        acc_attached = ''
        
        if User.objects.filter(EmailId=user):
            u = User.objects.filter(EmailId=user)[0]

            if User_Account.objects.filter(acc = account).filter(user=u.id):
                acc_attached = u.password 

        return (six.text_type(account) + six.text_type(user) + acc_attached + six.text_type(timestamp))

    def _num_seconds(self, dt):
        return int((dt - datetime(2001, 1, 1)).total_seconds())

    def _now(self):
        return datetime.now() 


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        pwd = user.password
        return (six.text_type(user.pk) + pwd + six.text_type(timestamp)) +  six.text_type(user.is_active)

class ZipGuid(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) +  six.text_type(user.is_active)


def decode(uid):
    uid = str(force_text(urlsafe_base64_decode(uid)))
    x = uid.split('<#>')
    user = x[0].split(':')[1]
    account = int(x[1].split(':')[1]) 
    return user, account


zip_guid = ZipGuid()
account_activation_token = AccountActivationTokenGenerator()
default_token_generator = AccountTokenGenerator()