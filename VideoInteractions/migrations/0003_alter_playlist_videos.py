# Generated by Django 5.0.3 on 2024-03-26 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VideoInteractions', '0002_alter_playlist_videos'),
        ('Videos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='videos',
            field=models.ManyToManyField(blank=True, to='Videos.video'),
        ),
    ]