from django.urls import path
from Users import views

urlpatterns = [path('', views.user_profile, name='user_profile'),
               path('register/', views.register_handler, name='register_handler'),
               path('login/', views.login_handler, name='login_handler')]
