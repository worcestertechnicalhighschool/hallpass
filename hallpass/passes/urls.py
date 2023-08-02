from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.bathroom_selector, name='bathroom_selector'),
    path('bathroom/<int:pk>/', views.bathroom, name='bathroom'),
]