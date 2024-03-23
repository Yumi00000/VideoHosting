from django.urls import path

from Videos import views

urlpatterns = [
    path('', views.videos_page, name='index'),
    path('upload/', views.upload_video, name='upload_video'),
    path('<video_name>/', views.video_page, name='video_page'),
]
