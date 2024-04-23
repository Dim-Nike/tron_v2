# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('<str:room_name>/', views.JoinChatView.as_view(), name='room'),
]
