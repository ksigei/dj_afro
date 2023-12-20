from django.contrib import admin

# Register your models here.
from .models import Movie, Subscription, UserProfile

# add search fields to the admin panel
class MovieAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description']

# register the models
admin.site.register(Movie, MovieAdmin)
admin.site.register(Subscription)
admin.site.register(UserProfile)


