from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('registration/', views.registration, name='registration'),
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('user/<str:username>', views.user_page_view, name='user_detail'),
    path('chat/<str:username>', views.chat_view, name='chat'),
    path('edit/', views.edit, name='edit')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_URL)
