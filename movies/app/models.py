from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'phone_number']  # Fields required during user creation

    def __str__(self):
        return self.email

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.TextField()
    languages = models.CharField(max_length=255)
    series_or_movie = models.CharField(max_length=50)
    hidden_gem_score = models.FloatField(null=True, blank=True)
    country_availability = models.TextField()
    runtime = models.CharField(max_length=50)
    director = models.CharField(max_length=255, null=True, blank=True)
    writer = models.CharField(max_length=255, null=True, blank=True)
    actors = models.TextField(null=True, blank=True)
    imdb_score = models.FloatField(null=True, blank=True)
    awards_received = models.IntegerField(null=True, blank=True)
    awards_nominated_for = models.IntegerField(null=True, blank=True)
    boxoffice = models.CharField(max_length=50, null=True, blank=True)
    release_date = models.CharField(max_length=50, null=True, blank=True)
    netflix_link = models.URLField(null=True, blank=True)
    imdb_link = models.URLField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    imdb_votes = models.IntegerField(null=True, blank=True)
    poster = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

class Watchlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return f"{self.user.username}'s Watchlist"