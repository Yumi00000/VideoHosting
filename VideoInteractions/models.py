from django.db import models
from Videos.models import Video
from Users.models import User

class Playlist(models.Model):
    name = models.CharField(max_length=50)
    videos = models.ManyToManyField(Video, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video, blank=True)
    date = models.DateField()
