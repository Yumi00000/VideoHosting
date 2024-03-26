from django.urls import path

from VideoInteractions import views

urlpatterns = [
    path('<slug:playlist_slug>/', views.view_playlist, name='view_playlist'),
    path('create/<int:video_id>/', views.create_playlist, name='create_playlist'),
    path('add/<slug:playlist_slug>/<int:video_id>/', views.add_to_playlist, name='add_to_playlist')
]
