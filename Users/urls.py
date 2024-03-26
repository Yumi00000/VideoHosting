from django.urls import path
from Users import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.user_profile, name='user'),
    path('videos/<username>/', views.user_info, name='user_profile'),
    path('register/', views.register_handler, name='register_handler'),
    path('login/', views.login_handler, name='login_handler'),
    path('activate/<user_signed>', views.activate, name='activate'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'),
         name='password_change'),


]
