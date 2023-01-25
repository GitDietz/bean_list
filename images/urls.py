from django.urls import path

from .views import index_view, upload_view

app_name = 'images'

urlpatterns = [
    path('all', index_view, name='all'),
    path('upload', upload_view, name='upload'),
]