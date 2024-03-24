# Generated by Django 5.0.3 on 2024-03-24 21:07

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(choices=[('G', 'Games'), ('E', 'Entertainments'), ('N', 'News')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=268)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('video', models.FileField(upload_to='videos')),
                ('thumbnail', models.ImageField(null=True, upload_to='thumbnails')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=268)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('watchers_count', models.IntegerField(default=0)),
                ('comments_count', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='Videos.category')),
                ('comments', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Videos.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LikesAndDislikes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('like', models.BooleanField(default=False)),
                ('dislike', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_likes_and_dislikes', to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_likes_and_dislikes', to='Videos.video')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_comments', to='Videos.video'),
        ),
    ]
