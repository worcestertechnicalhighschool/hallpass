from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dest', views.destination_selector, name='destination_selector'),
    path('destination/<int:pk>/', views.destination, name='destination'),
]