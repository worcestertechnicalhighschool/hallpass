from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.destination_selector, name='destination_selector'),
    path('destination/<int:pk>/', views.destination, name='destination'),
]