from django.urls import re_path

from lists import api

urlpatterns = [
    re_path(route=r'^lists/(\d+)/$', view=api.list, name='api_list'),
]