from celery import shared_task
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.signing import BadSignature, Signer
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from Users.forms import RegisterForm, CustomUserChangeForm
from Users.models import CustomUser, Followers
from VideoInteractions.models import Playlist
from Videos.models import Video
from videoHosting import settings


@shared_task
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
                return redirect('/user/')
            else:
                # Authentication failed, handle the error
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm(request)

    return render(request, 'login.html', {'form': form})


def logout_handler(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.POST.get('yes'):
            auth.logout(request)

        return redirect('/')
    return render(request, 'logout_handler.html')


def user_profile(request, username):
    user_id = request.user.id
    user = CustomUser.objects.get(username=username)
    videos = Video.objects.filter(user_id=user.id)
    user.followers_count = Followers.objects.filter(user_id=user.id, is_follow=True).count()
    user.followings_count = Followers.objects.filter(following_id=user.id, is_follow=True).count()
    user.save()
    return render(request, 'user_profile.html', {'user': user, 'videos': videos, 'user_id': user_id})


@login_required(login_url='/user/login/')
def user_cabinet(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(f'/user/videos/{request.user.username}/')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'user_cabinet.html', {'form': form})


@login_required(login_url='/user/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


def followers_page_view(request, user_id):
    followers = Followers.objects.filter(user_id=user_id, is_follow=True).all()
    return render(request, 'followers_page.html', {'followers': followers})


def following_page_view(request, user_id):
    followings = Followers.objects.filter(following_id=user_id, is_follow=True).all()
    return render(request, 'following_page.html', {'followings': followings})
