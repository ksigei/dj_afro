from django.contrib import admin

# Register your models here.
from .models import Like

# add search fields to the admin panel
class LikeAdmin(admin.ModelAdmin):
    search_fields = ['user', 'movie']

# register the models
admin.site.register(Like, LikeAdmin)

