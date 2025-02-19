from django.contrib import admin
from .views import get_data, index, detail_view, get_event_calendar
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

urlpatterns = [
    path('', get_data, name='get-data'),
    path('index/', index, name='index'),
    path('detail/', detail_view, name='detail'),
    path('event_calendar/<int:year>/<int:month>/', get_event_calendar, name='get_event_calendar'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)