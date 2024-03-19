from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    birthday = models.DateField()
    gender = models.CharField(max_length=20, choices=(('M', 'Male'), ('F', 'Female'), ('P', 'Preferred not to say')),
                              default='P')
    phone_number = models.IntegerField()
    followers_count = models.IntegerField(default=0)
    followings_count = models.IntegerField(default=0)

    def __str__(self):
        return self.id
