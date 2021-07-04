from django.urls import path
from django.conf.urls import url

from .InvitingContributors.views import *
from .PasswordReset.views import *
from .index import NotificationView

urlpatterns = [
    path('Acutes/SendNotification/', NotificationView.as_view()),
    
    path('Acutes/Reset/<uidb64>/<token>/', PasswordResetConfirm, name="password_reset_confirm"),
    path('Acutes/Reset/password_reset_done/', PasswordResetDone, name='password_reset_done'),
    path('Acutes/Reset/password_reset_complete/', PasswordResetComplete, name='password_reset_complete'),

    path('Acutes/SendInvite/<uidb64>/<token>', ContributorConfirm, name="contributor_confirm"),

]