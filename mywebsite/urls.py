from django.contrib import admin
from django.urls import path, include

from . import views
from person_detector import views as viewsPersonDetector

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('person-detector/', include('person_detector.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)