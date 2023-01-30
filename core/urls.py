from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.urls import path, include, re_path


from core import settings
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('images/', include('images.urls')),
    path('admin/', admin.site.urls),
    # path('users/', include('allauth.urls', namespace='users')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicons/favicon.ico'))),
    re_path(r'^accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
