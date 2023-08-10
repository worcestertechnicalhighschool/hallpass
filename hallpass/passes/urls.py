from django.urls import path, include
from . import views
from . import views_static as vs

urlpatterns = [
    path('', views.dashboard, name='select'), # CHANGE name to dashboard
    path('monitor_destinations', views.monitor_destinations, name='monitor'),

    # Static Pages required for OAuth and SEO
    path('about/', vs.about, name='about'),
    path('contact/', vs.contact, name='contact'),
    path('help/', vs.help, name='help'),
    path('robots.txt', vs.robots, name='robots'),
    path('privacy/', vs.privacy, name='privacy'),
    path('terms/', vs.terms, name='terms'),

]