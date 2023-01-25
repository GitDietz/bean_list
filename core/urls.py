from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from core import settings
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('images/', include('images.urls')),
    path('admin/', admin.site.urls),
    # path('users/', include('allauth.urls', namespace='users')),
    re_path(r'^accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
