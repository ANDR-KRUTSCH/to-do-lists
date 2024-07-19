from django.urls import re_path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    re_path(route=r'^send_login_email$', view=views.send_login_email, name='send_login_email'),
    re_path(route=r'^login$', view=views.login, name='login'),
    re_path(route=r'^logout$', view=LogoutView.as_view(template_name = "home.html"), name='logout'),
]