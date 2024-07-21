from django.urls import re_path

from lists import api

urlpatterns = [
    re_path(route=r'^lists/(\d+)/get_items$', view=api.get_items, name='get_items'),
    re_path(route=r'^lists/(\d+)/post_item$', view=api.post_item, name='post_item'),
]