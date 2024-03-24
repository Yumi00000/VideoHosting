from celery import shared_task
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.signing import BadSignature, Signer
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from Users.forms import RegisterForm
from Users.models import CustomUser
from Videos.models import Video
from videoHosting import settings


@shared_task(serializer='json')
def send_activation_email(base_url, user_id):
    user_signed = Signer().sign(user_id)
    signed_url = base_url + f"user/activate/{user_signed}"
    send_mail(
        subject="Registration complete",
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
            form.instance.is_active = False
            form.save()
            send_activation_email.delay(request.build_absolute_uri('/'), form.instance.id)
            return redirect('/user/login/')
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form})


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
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authentication successful, log in the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page
                return redirect('user_profile')
            else:
                # Authentication failed, handle the error
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm(request)

    return render(request, 'login.html', {'form': form})


def user_info(request, username):
    user = CustomUser.objects.get(username=username)
    videos = Video.objects.filter(user_id=user.id)
    return render(request, 'user_profile.html', {'user': user, 'videos': videos})


@login_required(login_url='/user/login/')
def user_profile(request):
    return HttpResponseRedirect('OK')
