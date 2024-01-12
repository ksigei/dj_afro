from django.contrib import admin
from .models import Movie, Subscription, UserProfile, Person, Contribution, Rating, Transaction, Genre

# Register your models here.
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'duration')
    list_filter = ('release_date',)
    search_fields = ('title', 'description')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription', 'created_at')
    list_filter = ('subscription', 'created_at')
    search_fields = ('user__username',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    list_filter = ('role',)
    search_fields = ('name',)

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('person', 'movie', 'role')
    list_filter = ('role',)
    search_fields = ('person__name', 'movie__title')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating')
    list_filter = ('rating',)
    search_fields = ('user__username', 'movie__title')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'movie')
    list_filter = ('amount', 'movie')
    search_fields = ('user__username',)
    