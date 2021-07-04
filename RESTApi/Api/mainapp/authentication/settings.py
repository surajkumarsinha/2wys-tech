from datetime import timedelta

from django.conf import settings


DEFAULTS = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

REFRESH_TOKEN_SECRET = '8JgGpIojyqsvRkMVGlIHAQws4xaJBHSySr1PZVfzY64as420CSnscaTyqCNWzJH'