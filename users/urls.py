"""Define regular values for url"""

from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    #Adding default URL auth (authentifications)
    path('', include('django.contrib.auth.urls')),
    #Reestration page
    path('register/', views.register, name='register'),
]
