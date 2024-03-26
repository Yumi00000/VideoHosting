from django.db import models
from django.utils import timezone

from Videos.models import Video
from Users.models import CustomUser


class Playlist(models.Model):
    name = models.CharField(max_length=50)
    videos = models.ManyToManyField(Video, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)


class History(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, blank=True)
    date = models.DateField(default=timezone.now)
