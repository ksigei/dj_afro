from django.contrib import admin

# Register your models here.
from .models import Comment

# add search fields to the admin panel
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['user', 'movie']

# register the models
admin.site.register(Comment, CommentAdmin)
