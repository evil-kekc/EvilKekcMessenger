from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('registration/', views.registration, name='registration'),
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search')
]
