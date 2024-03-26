from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from VideoInteractions.models import Playlist
from Videos.models import Video


def create_playlist(request, video_id):
    if request.method == 'POST':
        playlist_name = request.POST.get('playlist_name')
        if not playlist_name:
            return HttpResponseBadRequest("Playlist name is required.")

        playlist = Playlist.objects.create(user=request.user, slug=slugify(playlist_name), name=playlist_name)
        playlist.save()
        video = Video.objects.get(id=video_id).name
        return redirect(f'/{video}/')
    else:
        return render(request, 'create_playlist.html')


@require_POST
def add_to_playlist(request, playlist_slug, video_id):
    playlist = Playlist.objects.get(slug=playlist_slug)
    video = get_object_or_404(Video, id=video_id)
    playlist.videos.add(video)

    return redirect(f'/playlist/{playlist_slug}/')


def view_playlist(request, playlist_slug):
    playlist = get_object_or_404(Playlist, slug=playlist_slug)
    return render(request, 'view_playlist.html', {'playlist': playlist})
