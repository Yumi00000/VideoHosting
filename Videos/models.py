from django.db import models
from Users.models import CustomUser


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.FileField(upload_to='videos', null=False)
    thumbnail = models.ImageField(upload_to='thumbnails', null=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=268)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    watchers_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='videos')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category')
    comments = models.ManyToManyField('Comment', blank=True, related_name='comments')

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='video_comments')
    comment = models.CharField(max_length=268)
    date = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, choices=(('G', 'Games'), ('E', 'Entertainments'), ('N', 'News')))

    def __str__(self):
        return self.name
