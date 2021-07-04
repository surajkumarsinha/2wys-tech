import datetime
import json
# from axes.helpers import get_client_username
from importlib import import_module
from functools import partial
from django.db import transaction
from django.contrib.auth import user_logged_in, get_user_model
from ..authentication.models import User
import jwt
from django.conf import settings
from django.http import HttpResponse
from django.utils.cache import patch_cache_control
from rest_framework import status as status_codes
from ..authentication.settings import REFRESH_TOKEN_SECRET
from rest_framework import exceptions
from rest_framework.settings import api_settings


def get_jwt_tokens(user):
    refresh_token = generate_refresh_token(user)
    access_token = generate_access_token(user, refresh_token)
    return {'refresh_token': refresh_token, 'access_token': access_token}


def generate_access_token(user, refresh_token):

    if not refresh_token:
        raise exceptions.PermissionDenied('No refresh token provided')
    else:
        access_token_payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=20),
            'iat': datetime.datetime.utcnow(),
        }
        access_token = jwt.encode(access_token_payload,
                                  settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
        return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, REFRESH_TOKEN_SECRET, algorithm='HS256').decode('utf-8')

    return refresh_token


def access_token_refresh(request):
    User = get_user_model()
    refresh_token = request.COOKIES.get('refreshtoken')
    payload = jwt.decode(refresh_token, REFRESH_TOKEN_SECRET, algorithms=['HS256'])
    user = User.objects.filter(id=payload['user_id']).first()
    access_token = generate_access_token(user, refresh_token)

    return {
        'access_token': access_token,
        'id': user.id
        }


def client_ip(request):
    """
    Get clients IP address 
    :Parameters:
        request: (obj)
    :Returns:
       ip: (str) IP Address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    elif x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def make_response(success=True, data=None, status=None):
    if not status:
        status = status_codes.HTTP_200_OK if success else status_codes.HTTP_400_BAD_REQUEST

    response = HttpResponse(json.dumps(data), content_type="application/json", status=status)
    # block user
    # on invalid attempt inc the invalidLogin cookie -> alive for 15 min
    # check if it is the same user. if max 5 illegal attempt in 15 mins.
    # create block cookie which stores value of user id => lives for 10 min
    # on correct signin delete this cookie

    patch_cache_control(response, no_cache=True, no_store=True)
    return response


def login_user(request, user):
    User.objects.filter(pk=user.id).update(auth_change_failures=0)
    user.auth_change_failures = 0
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    return get_jwt_tokens(user)
    # print(User.objects.filter(pk=user.id))


# def generate_axes_lockout_response(request, credentials):
#     enqueue(
#         "authentication.tasks:force_password_reset", get_client_username(request, credentials)
#     )
#     error_message = (
#         f"Too many failed login attempts, check your email to choose a new password."
#     )
#     return make_response(data={api_settings.NON_FIELD_ERRORS_KEY: error_message}, status=403)


def get_partial(task, *args, **kwargs):
    imported_task = task

    if isinstance(task, str):
        module, attr = task.split(":")

        # Have the option to import here to avoid circular dependencies that the tasks are fraught with
        imported_task = getattr(import_module(module), attr)

    return partial(imported_task, *args, **kwargs)


def enqueue(task, *args, **kwargs):
    partial_task = get_partial(task, *args, **kwargs)

    # Since the calling code could have modified the same records that
    #   the worker needs, make sure the database has committed the
    #   new data before proceeding so that the worker has access to
    #   the data.
    transaction.on_commit(partial_task)