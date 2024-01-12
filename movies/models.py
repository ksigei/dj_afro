from django.db import models
from django.contrib.auth.models import User
# from likes.models import Like
# from comments.models import Comment
import uuid

class Person(models.Model):
    roles = (
        ('starring', 'Starring'),
        ('actor', 'Actor'),
        ('director', 'Director'),
        ('writer', 'Writer'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    bio = models.TextField(default='No bio')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    role = models.CharField(max_length=255, choices=roles, default='actor')

    def __str__(self):
        return self.name

class Genre(models.Model):
    genre_choices = (
        ('action', 'Action'),
        ('adventure', 'Adventure'),
        ('comedy', 'Comedy'),
        ('crime', 'Crime'),
        ('drama', 'Drama'),
        ('fantasy', 'Fantasy'),
        ('historical', 'Historical'),
        ('horror', 'Horror'),
        ('mystery', 'Mystery'),
        ('romance', 'Romance'),
        ('science_fiction', 'Science Fiction'),
        ('thriller', 'Thriller'),
        ('western', 'Western'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, choices=genre_choices)

    def __str__(self):
        return self.name

class Movie(models.Model):
    quality_choices = (
        ('HD', 'HD'),
        ('SD', 'SD'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre, related_name='movies', blank=True)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/')
    trailer = models.FileField(upload_to='trailers/', null=True, blank=True)

    to_slider = models.BooleanField(default=False)
    quality = models.CharField(max_length=255, choices=quality_choices, default='HD')

    contributors = models.ManyToManyField(Person, through='Contribution')
    ratings = models.ManyToManyField(User, through='Rating')
    

    def __str__(self):
        return self.title
    
    def get_likes(self):
       return Like.objects.filter(movie_id=self.id).count()

class Contribution(models.Model):
    role_choices = (
        ('starring', 'Starring'),
        ('actor', 'Actor'),
        ('director', 'Director'),
        ('writer', 'Writer'),
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=role_choices, default='starring')

    def __str__(self):
        return f'{self.person.name} - {self.movie.title} ({self.role})'

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.user.username} - {self.movie.title} ({self.rating})'

class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    watchlist = models.ManyToManyField(Movie, related_name='watchlist', blank=True)

    def __str__(self):
        return self.user.username

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} liked'


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.movie.title} ({self.timestamp})'
    
