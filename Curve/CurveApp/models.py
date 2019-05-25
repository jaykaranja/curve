from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_name = models.CharField(max_length=45)
    album_artist = models.CharField(max_length=45)
    album_cover = models.FileField()
    def get_absolute_url(self):
        return reverse('CurveApp:index')
    
class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_name = models.CharField(max_length=45)
    song_artist = models.CharField(max_length=45)
    song = models.FileField()
