from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    genres = models.TextField()
    nations = models.TextField()
    poster = models.CharField(max_length=300)
    content = models.TextField()