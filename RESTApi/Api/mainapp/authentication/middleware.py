import json

from django.contrib.auth import logout, get_user_model
from django.contrib import messages
import datetime
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder


class SessionIdleTimeout:
    """Middleware class to timeout a session after a specified time period.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)

        return response

    def process_request(self, request):

        if request.headers.get('Cookie'):

            current_datetime = {
                "date-time": datetime.datetime.now(),
            }
            if 'last_activity' not in request.session:
                request.session['last_activity'] = json.dumps(current_datetime, indent=4, sort_keys=True, default=str)
            else:
                print('Time is already there')

            print(request.session['last_activity'])

        return None

