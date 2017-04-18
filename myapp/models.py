from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class SalesTrackerUser(models.Model):
    user_name = models.TextField()
    password = models.TextField()
    phone = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    status = models.TextField()

    class Meta:
        managed = True
        db_table = 'user_register'

    def saveuser(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.user_name
		
class UserLocation(models.Model):
    phone = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()
    address = models.TextField(default=' ')
    created_date = models.DateTimeField(default=timezone.now)
    city = models.TextField(default=' ');
    state = models.TextField(default=' ');
    country = models.TextField(default=' ');


    class Meta:
        managed = True
        db_table = 'user_location'

    def saveuser(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.phone
