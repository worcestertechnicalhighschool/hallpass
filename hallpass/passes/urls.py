from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.select_destinations, name='select'),
    path('monitor_destinations', views.monitor_destinations, name='monitor'),
]