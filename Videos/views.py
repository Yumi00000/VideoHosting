import os
import subprocess

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from videoHosting import settings
from Videos.forms import VideoUploadForm
from Videos.models import Video, Comment


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
        if video.thumbnail is None:
            thumbnail_name = os.path.splitext(os.path.basename(video_path))[0] + '.jpg'
            thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', thumbnail_name)

            command = ['ffmpeg', '-i', video_path, '-ss', '00:00:00.000', '-vframes', '1', thumbnail_path]
            try:
                subprocess.run(command, check=True)

                video.thumbnail = os.path.join('thumbnails', thumbnail_name)
                video.save()
            except subprocess.CalledProcessError as e:
                print(f"Error generating thumbnail: {e}")
        pass
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


def video_page(request, video_name):
    video = Video.objects.get(name=video_name)
    comments = Comment.objects.filter(video_id=video.id).order_by('-date')
    video.watchers_count += 1
    video.save()

    if request.method == 'POST':
        if request.user.is_authenticated:
            content = request.POST.get('comment')
            if content:
                video.comments_count += 1
                video.save()
                comment = Comment.objects.create(user=request.user, video_id=video.id, comment=content)
                comment.save()

            # Get the action parameter from the POST request
            action = request.POST.get('action')
            if action == 'like':
                video.likes += 1
            elif action == 'dislike':
                video.dislikes += 1
            video.save()
            comments = Comment.objects.filter(video_id=video.id).order_by('-date')
            comments_html = render_to_string('comments_section.html', {'comments': comments, 'video': video})
            response_data = {
                'comments_html': comments_html,
                'likes': video.likes,
                'dislikes': video.dislikes
            }
            return JsonResponse(response_data)
        else:
            messages.error(request, 'Please log in to add a comment.')

    return render(request, 'video_page.html', {'video': video, 'comments': comments})
