# Generated by Django 5.0.3 on 2024-03-26 18:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Videos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="video",
            field=models.FileField(
                upload_to="videos",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["MOV", "avi", "mp4", "webm", "mkv"]
                    )
                ],
            ),
        ),
    ]
