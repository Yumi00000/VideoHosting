from django.urls import path

from VideoInteractions import views

urlpatterns = [
    path('', views.all_playlists, name='all_playlists'),
    path('videos/<slug:playlist_slug>/', views.view_playlist, name='view_playlist'),
    path('create/', views.create_playlist, name='create_playlist'),
    path('add/<slug:playlist_slug>/<int:video_id>/', views.add_to_playlist, name='add_to_playlist'),
    path('remove/<slug:playlist_slug>/<int:video_id>/', views.remove_from_playlist, name='remove_from_playlist')

]
