from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from django.contrib import auth
from accounts.models import Token
from accounts.authentication import PasswordlessAuthenticationBackend

# Create your views here.
def send_login_email(request: HttpRequest) -> HttpResponse:
    email = request.POST.get('email')
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(reverse('login') + f'?token={token.uid}')
    message = f'Use this link to log in:\n\n{url}'
    send_mail(
        subject='Your login link for Superlists',
        message=message,
        from_email='andr.krutsch@gmail.com',
        recipient_list=[email]
    )
    messages.success(request, 'Check your email, we sent link, use this link to log in.')
    return redirect('/')

def login(request: HttpRequest):
    user = auth.authenticate(request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')