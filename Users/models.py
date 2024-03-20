from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    birthday = models.DateField()
    gender = models.CharField(max_length=20, choices=(('M', 'Male'), ('F', 'Female'), ('P', 'Preferred not to say')),
                              default='P')
    phone_number = models.CharField(max_length=20)
    followers_count = models.IntegerField(default=0)
    followings_count = models.IntegerField(default=0)
    is_logged = models.BooleanField(default=False)

    # Specify unique related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuse',  # Change this related_name to avoid clashes
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',  # Change this related_name to avoid clashes
        related_query_name='user',
    )

    def __str__(self):
        return self.username
