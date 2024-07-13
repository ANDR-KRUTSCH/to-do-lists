from django.urls import re_path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    re_path('^send_login_email$', views.send_login_email, name='send_login_email'),
    re_path('^login$', views.login, name='login'),
    re_path('^logout$', LogoutView.as_view(template_name = "home.html"), name='logout'),
]