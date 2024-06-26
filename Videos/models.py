from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.db import models
from Users.models import CustomUser


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.FileField(
        upload_to="videos",
        null=False,
        validators=[FileExtensionValidator(allowed_extensions=["MOV", "avi", "mp4", "webm", "mkv"])],
    )

    thumbnail = models.ImageField(upload_to="thumbnails", null=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=268)
    date = models.DateTimeField(auto_now_add=True)
    watchers_count = models.IntegerField(default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="videos")
    category = models.CharField(max_length=50, choices=(("G", "Games"), ("E", "Entertainments"), ("N", "News")))

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="video_comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="video_comments")
    comment = models.CharField(max_length=268)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)


class LikesAndDislikes(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_likes_and_dislikes")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="video_likes_and_dislikes")
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
