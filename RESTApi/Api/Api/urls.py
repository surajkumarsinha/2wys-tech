"""Api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('mainapp.authentication.urls')),
    path('api/', include('mainapp.userProfile.urls')),
    path('api/', include('mainapp.fileSystem.urls')),
    path('api/', include('mainapp.signCreation.urls')),
    path('api/', include(('mainapp.notifications.urls', 'web'), namespace='web')),
    path('api/', include('mainapp.signerWebSocket.urls')),
    path('api/Acutes/', include('djoser.urls.base')),
    # post ->/users/set_password/
    # get ->/users/ -> List of all the users -> permission isAdmin
]
# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
