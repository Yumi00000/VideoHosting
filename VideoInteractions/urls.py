from django.urls import path

from VideoInteractions import views

urlpatterns = [
    path('<int:user_id>/', views.all_user_playlists, name='all_playlists'),
    path('create/', views.create_playlist, name='create_playlist'),
    path('add/<slug:playlist_slug>/<int:video_id>/', views.add_to_playlist, name='add_to_playlist'),
    path('remove/<slug:playlist_slug>/<int:video_id>/', views.remove_from_playlist, name='remove_from_playlist'),
    path('videos/<slug:playlist_slug>/', views.view_playlist, name='view_playlist'),
    path('remove/<slug:playlist_slug>/', views.remove_playlist, name='remove_playlist')

]
