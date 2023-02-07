from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views

from .views_list import (items_list, item_create, item_edit,
                         list_detail, user_lists)
from .views_merchant import merchant_create, merchant_list, merchant_update, merchant_delete

app_name = 'lists'

urlpatterns = [
    # lists
    path('user_lists', user_lists, name='user_lists'),
    # path(group_remove_self/(?P<pk>\d+)', StockNoteCreateView.as_view(), name='note_create'),
    # path('note_update_ajax', note_update_ajax, name='note_update_ajax'),
    path('list_create', list_detail, name='list_create'),
    re_path(r'list_detail/(?P<pk>\d+)/(?P<list_obj>)', list_detail, name='list_detail'),

    # item urls
    re_path(r'item_create/(?P<pk>\d+)', item_create, name='item_create'),
    re_path(r'item_edit/(?P<pk>\d+)', item_edit, name='item_edit'),
    re_path(r'items_list/(?P<pk>\d+)', items_list, name='items_list'),

    # merchant
    re_path(r'merchant_create/(?P<pk>\d+)', merchant_create, name='merchant_create'),
    re_path(r'merchant_list/(?P<pk>\d+)', merchant_list, name='merchant_list'),
    re_path(r'merchant_edit/(?P<pk>\d+)', merchant_update, name='merchant_update'),
    re_path(r'merchant_delete/(?P<pk>\d+)', merchant_delete, name='merchant_delete'),

    ]
