from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.urls import reverse

from accounts.models import Token

# Create your views here.
def send_login_email(request: HttpRequest) -> HttpResponseRedirect:
    email = request.POST.get('email')
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(location=reverse(viewname='login') + f'?token={token.uid}')
    message = f'Use this link to log in:\n\n{url}'
    send_mail(
        subject='Your login link for Superlists',
        message=message,
        from_email='andr.krutsch@gmail.com',
        recipient_list=[email]
    )
    messages.success(request=request, message='Check your email, we sent link, use this link to log in.')
    return redirect(to='/')

def login(request: HttpRequest) -> HttpResponseRedirect:
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request=request, user=user)
    return redirect(to='/')