from django.contrib import admin
from .views import get_data
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

urlpatterns = [
    path('', get_data, name='get-data'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)