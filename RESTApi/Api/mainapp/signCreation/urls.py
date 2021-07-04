from django.urls import path
from .views import CreateSignView, DisplaySignView, EditSignView, DeleteSignView, GetSignView

urlpatterns = [
    path('Acutes/CreateSign/', CreateSignView.as_view(), name='CreateSignView'),
    path('Acutes/DisplaySign/', DisplaySignView.as_view(), name='DisplaySignView'),
    path('Acutes/EditSign/', EditSignView.as_view(), name='EditSignView'),
    path('Acutes/DeleteSign/', DeleteSignView.as_view(), name='DeleteSignView'),
    path('Acutes/GetSign/', GetSignView.as_view(), name='GetSignView'),
]