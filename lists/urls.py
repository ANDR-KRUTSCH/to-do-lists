from django.urls import re_path

from . import views

urlpatterns = [
    # re_path(route=r'^new$', view=views.new_list, name='new_list'),
    re_path(route=r'^new$', view=views.NewList.as_view(), name='new_list'),
    # re_path(route=r'^(\d+)/$', view=views.view_list, name='view_list'),
    re_path(route=r'^(\d+)/$', view=views.ViewList.as_view(), name='view_list'),
    # re_path(route=r'^users/(.+)/$', view=views.my_lists, name='my_lists'),
    re_path(route=r'^users/(.+)/$', view=views.MyLists.as_view(), name='my_lists'),
    # re_path(route=r'^(\d+)/share$', view=views.share_list, name='share_list'),
    re_path(route=r'^(\d+)/share$', view=views.ShareList.as_view(), name='share_list'),
]