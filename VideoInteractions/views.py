from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from VideoInteractions.models import Playlist
from Videos.models import Video


@login_required(login_url='/user/login/')
def create_playlist(request):
    if request.method == 'POST':
        playlist_name = request.POST.get('playlist_name')
        if not playlist_name:
            return HttpResponseBadRequest("Playlist name is required.")

        playlist = Playlist.objects.create(user=request.user, slug=slugify(playlist_name), name=playlist_name)
        playlist.save()
        return redirect('/')
    else:
        return render(request, 'create_playlist.html')


@require_POST
def add_to_playlist(request, playlist_slug, video_id):
    playlist = Playlist.objects.get(slug=playlist_slug)
    video = get_object_or_404(Video, id=video_id)
    if video in playlist.videos.all():
        return HttpResponse("Okay, this video has already been added to your playlist.")
    else:
        playlist.videos.add(video)
        return HttpResponse('Video added')


def view_playlist(request, playlist_slug):
    playlist = get_object_or_404(Playlist, slug=playlist_slug)
    return render(request, 'view_playlist.html', {'playlist': playlist, 'user': request.user})


def all_user_playlists(request, user_id):
    if request.user.is_authenticated and request.user.id == user_id:
        playlists = Playlist.objects.filter(user_id=request.user.id).all
        return render(request, 'all_user_playlists.html', {"playlists": playlists})
    else:
        playlists = Playlist.objects.filter(user_id=user_id).all
        return render(request, 'all_user_playlists.html', {"playlists": playlists})


@require_POST
def remove_from_playlist(request, playlist_slug, video_id):
    playlist = get_object_or_404(Playlist, slug=playlist_slug)
    playlist.videos.remove(video_id)
    return HttpResponse('Video removed')
