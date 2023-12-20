from django.contrib import admin

# Register your models here.
from .models import Product, Order, Review

# add search fields to the admin panel
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']

class OrderAdmin(admin.ModelAdmin):
    search_fields = ['user', 'products']

class ReviewAdmin(admin.ModelAdmin):
    search_fields = ['user', 'product']

# register the models
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)



