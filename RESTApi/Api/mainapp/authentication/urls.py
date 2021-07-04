from django.urls import path
from rest_framework import routers
from .views import SignInView, SignUpView, SignOutView, token_refresh, GetUserAccounts


router = routers.DefaultRouter()

urlpatterns = [
    path('Acutes/SignUp/', SignUpView.as_view(), name='SignUp'),
    # path('Acutes/SignUp/<uidb64>/', SignUpView.as_view(), name='SignUp'),
    path('Acutes/SignIn/', SignInView.as_view(), name='SignIn'),
    path('Acutes/SignOut/', SignOutView.as_view(), name='SignOut'),
    path('Acutes/GetAllUserAccounts/', GetUserAccounts.as_view(), name='GetUserAccounts'),
    path('Acutes/Refresh/', token_refresh),
]
