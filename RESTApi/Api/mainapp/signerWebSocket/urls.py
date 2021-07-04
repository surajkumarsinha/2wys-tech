from django.urls import path
from .views import FileSendView

urlpatterns = [
    path('Acutes/SendFile/', FileSendView.as_view()),
]