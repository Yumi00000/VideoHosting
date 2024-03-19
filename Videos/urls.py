from django.urls import path

from Videos import views

urlpatterns = [path('', views.videos, name='index')]