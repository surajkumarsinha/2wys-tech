from django.urls import path
from .views import LoadProfileView, EditProfileView, ChangePasswordView, GetUserDetailView

urlpatterns = [
    path('Acutes/LoadProfile/', LoadProfileView.as_view(), name='LoadProfile'),
    path('Acutes/EditProfile/', EditProfileView.as_view(), name='EditProfile'),
    path('Acutes/ChangePassword/', ChangePasswordView.as_view(), name='ChangePassword'),
    path('Acutes/GetUserDetail/', GetUserDetailView.as_view(), name='GetUserDetailView'),
]
