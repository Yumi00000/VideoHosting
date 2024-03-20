from celery import shared_task
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.signing import BadSignature, Signer
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from Users.forms import RegisterForm, LoginForm
from Users.models import CustomUser
from videoHosting import settings


@shared_task(serializer='json')
def send_activation_email(base_url, user_id):
    user_signed = Signer().sign(user_id)
    signed_url = base_url + f"/activate/{user_signed}"
    send_mail(
        subject=("Registration complete"),
        message=("Click here to activate your account: " + signed_url),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[CustomUser.objects.get(pk=user_id).email],
        fail_silently=False,
    )
    return "sent activation email"


def register_handler(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if CustomUser.objects.filter(email=form.cleaned_data['username']).exists() or \
                    form.cleaned_data['password'] != \
                    form.cleaned_data['confirm_password']:
                messages.error(request, 'Data already registered or passwords didn`t match')

            form.instance.is_active = False
            form.save()
            email = request.POST.get('email')
            send_activation_email.delay(request.build_absolute_uri('/'), form.instance.id)
            return redirect('/user/login/')
    return render(request, 'registration.html', {'form': RegisterForm()})


def activate(request, user_signed):
    try:
        user_id = Signer().unsign(user_signed)
    except BadSignature:
        return redirect("/user/login/")
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return redirect("/user/login/")
    user.is_active = True
    user.save()
    return redirect("/user/login/")


def login_handler(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            try:
                login(request, user)
                messages.success(request, 'Welcome ' + username + '!')
                return redirect('/user/')
            except BadSignature:
                messages.error(request, f'Data invalid. Please try again.')
                return redirect('/user/login/')
    return render(request, 'login.html', {'form': LoginForm()})


@login_required(login_url='/user/login/')
def user_profile(request):
    return HttpResponse('OK')
