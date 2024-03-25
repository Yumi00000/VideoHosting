import os
import subprocess

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from Users.models import Followers
from videoHosting import settings
from Videos.forms import VideoUploadForm
from Videos.models import Video, Comment, LikesAndDislikes


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
        if not video.thumbnail:
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
    return render(request, 'videos_page.html', {'videos': videos})


def video_page(request, video_name):
    video = get_object_or_404(Video, name=video_name)

    # Increment watchers_count and save the video
    video.watchers_count += 1
    video.save()

    # Get comments
    comments = Comment.objects.filter(video=video).order_by('-date')

    if request.method == 'POST':
        if request.user.is_authenticated:
            content = request.POST.get('comment')
            if content:
                # Create and save a new comment
                Comment.objects.create(user=request.user, video=video, comment=content)
                # Increment comments_count
                video.comments_count += 1
                video.save()

            # Toggle like/dislike
            action = request.POST.get('action')
            if action in ['like', 'dislike']:
                likes_obj, created = LikesAndDislikes.objects.get_or_create(user=request.user, video=video)
                if action == 'like':
                    likes_obj.like = not likes_obj.like
                    likes_obj.dislike = False
                else:
                    likes_obj.dislike = not likes_obj.dislike
                    likes_obj.like = False
                likes_obj.save()
            if action == 'follow':
                follows_obj, created = Followers.objects.get_or_create(user=video.user, following=request.user)
                follows_obj.is_follow = not follows_obj.is_follow

                follows_obj.save()
            follow_count = Followers.objects.filter(user=request.user, is_follow=True).count()
            likes = LikesAndDislikes.objects.filter(video=video, like=True).count()
            dislikes = LikesAndDislikes.objects.filter(video=video, dislike=True).count()

            # Get updated comments
            comments = Comment.objects.filter(video=video).order_by('-date')
            comments_html = render_to_string('comments_section.html', {'comments': comments, 'video': video})
            return JsonResponse(
                {'comments_html': comments_html, 'likes': likes, 'dislikes': dislikes, 'follow_count': follow_count})

        else:
            messages.error(request, 'Please log in to add a comment or like/dislike.')

    follow_count = Followers.objects.filter(user=request.user, is_follow=True).count()
    likes = LikesAndDislikes.objects.filter(video=video, like=True).count()
    dislikes = LikesAndDislikes.objects.filter(video=video, dislike=True).count()

    return render(request, 'video_page.html',
                  {'video': video, 'comments': comments, 'likes': likes, 'dislikes': dislikes,
                   'follow_count': follow_count})
