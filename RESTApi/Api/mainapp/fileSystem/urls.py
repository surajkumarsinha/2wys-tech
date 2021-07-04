from django.urls import path
from .views import (
    FileUploadView,
    FileDownloadView,
    LoadGrid,
    load_account_users,
    QuerysetConvert,
    GetSignedFile
    )

urlpatterns = [
    path('Acutes/Upload/', FileUploadView.as_view()),
    path('Acutes/Download/', FileDownloadView.as_view()),
    path('Acutes/ViewFile/', FileDownloadView.as_view()),
    path('Acutes/LoadGrid/', LoadGrid.as_view()),
    path('Acutes/LoadUserAccounts/', load_account_users.as_view()),
    path('Acutes/QueryAccountNames/', QuerysetConvert.as_view()), 
    path('Acutes/GetSignedFile/', GetSignedFile.as_view()), 
]
