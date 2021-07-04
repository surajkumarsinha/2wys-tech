import os
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w4cdyxa(c&juow#k#*1z&&&lwuux%%aau(mx_dxs*6y-1vh-y5'

DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'djoser',
    'rest_framework.authtoken',
    'corsheaders',
    # "rest_framework_recaptcha",
    'mainapp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'axes.middleware.AxesMiddleware',
    # 'authentication.middleware.SessionIdleTimeout',
]



SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60
SESSION_SAVE_EVERY_REQUEST = True

ROOT_URLCONF = 'Api.urls'

# os.path.join(BASE_DIR, 'mainapp/template')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_USER_MODEL = 'mainapp.User'

WSGI_APPLICATION = 'Api.wsgi.application'


# CORS_ORIGIN_WHITELIST = [
#     "http://localhost:9001",
#     "http://localhost:3000"
# ]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'account',
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'withCredentials',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'AcutesDRF',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',

    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        "OPTIONS": {"min_length": 4},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# --------------- REST Framework ------------------ #

REST_FRAMEWORK = {

       # Pagination Settings
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10, 
   
    # Authentication and Permissions
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # a custom authentication method
        'mainapp.authentication.authentication.SafeJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # make all endpoints private
    ),

    # Throttling Settings
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle'
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '100/day',
    #     'user': '1000/day'
    # },
    # 'DEFAULT_THROTTLE_CLASSES': (
    #     'rest_framework.throttling.UserRateThrottle',

    # ),
    # 'DEFAULT_THROTTLE_RATES': {
    #     'loginAttempts': '8/hr',
    #     'user': '1000/min',
    # },

}



# AUTHENTICATION_BACKENDS = [
#     # AxesBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
#     'axes.backends.AxesBackend',

#     # Django ModelBackend is the default authentication backend.
#     'django.contrib.auth.backends.ModelBackend',
# ]
# ------------- DJSOER config ----------------- #

DJOSER = {
    "SEND_ACTIVATION_EMAIL": False,
    "PASSWORD_RESET_CONFIRM_URL": "#/password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "#/username/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "#/activate/{uid}/{token}",
    'user_list': ['djoser.permissions.CurrentUserOrAdminOrReadOnly'],
    # "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": ["http://test.localhost/"],
}


# ------------------ JWT Auth ---------------------- #

JWT_AUTH = {"JWT_ALLOW_REFRESH": True}


# ------------------ Axes Config -------------------- #

# AXES_USERNAME_FORM_FIELD = "EmailId"
# AXES_COOLDOWN = 60
# AXES_LIMIT = 10
# AXES_RESET_ON_SUCCESS = True
# AXES_LOCKOUT_CALLABLE = "mainapp.authentication.utils.generate_axes_lockout_response"


# ----------- Notification Email Config ------------ #

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'suraj.useracc0519@gmail.com'
EMAIL_HOST_PASSWORD = 'suraj12345'
EMAIL_PORT = 587




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ------------------- Celery ----------------------- #

# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = TIME_ZONE


# Email Notification settings #
