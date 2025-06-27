# orionapp_project/urls.py

from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orionapp.urls')),  # Link to the app URLs
]
