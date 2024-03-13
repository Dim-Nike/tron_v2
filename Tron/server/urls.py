from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('', show_index, name='index')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)