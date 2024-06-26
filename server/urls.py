from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('', show_index, name='home'),
    path('login', show_login, name='login'),
    path('register', show_register, name='register'),
    path('chat', show_chat, name='chat'),
    path('profile', show_profile, name='profile'),
    path('set-idf-form', show_form_idf, name='set-idf-form')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)