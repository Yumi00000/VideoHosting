from django.urls import path

from Videos import views

urlpatterns = [
    path('', views.videos_page, name='index'),
    path('upload/', views.upload_video, name='upload_video'),
    path('edit/<int:video_id>/<int:user_id>', views.edit_video, name='edit_video'),
    path('video/<video_name>/', views.video_page, name='video_page'),
    path('remove/comment/<int:video_id>/<int:user_id>/<int:comment_id>/', views.remove_comment, name='remove_comment')
]
