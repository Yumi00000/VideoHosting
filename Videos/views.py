import os
import subprocess
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from videoHosting import settings
from Videos.forms import VideoUploadForm
from Videos.models import Video


@login_required(login_url='/user/login')
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            video_path = os.path.join(settings.MEDIA_ROOT, str(video.video))
            generate_thumbnail(video_path, video)

            return redirect('/')
    else:
        form = VideoUploadForm()
    return render(request, 'upload_video.html', {'form': form})


def generate_thumbnail(video_path, video):
    if os.path.exists(video_path):

        thumbnail_name = os.path.splitext(os.path.basename(video_path))[0] + '.jpg'
        thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', thumbnail_name)

        command = ['ffmpeg', '-i', video_path, '-ss', '00:00:00.000', '-vframes', '1', thumbnail_path]
        try:
            subprocess.run(command, check=True)

            video.thumbnail = os.path.join('thumbnails', thumbnail_name)
            video.save()
        except subprocess.CalledProcessError as e:
            print(f"Error generating thumbnail: {e}")
    else:
        print(f"Video file not found: {video_path}")


def videos_page(request):
    videos = Video.objects.all()
    category_param = request.GET.get('category')
    if category_param and category_param != 'all':
        videos = Video.objects.filter(category__name=category_param)
    for video in videos:
        print(video.thumbnail.url)
        print(video.video.url)
    return render(request, 'videos_page.html', {'videos': videos})

# def video_page(request, video_name):
#     videos = request.GET.get('video_name')
#     video = Video.objects.get(name=video_name)
#     if request.method == 'POST':
