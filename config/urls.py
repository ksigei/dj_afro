from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movies.urls')), 
    
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# dashboard title: Dj Afro 
# dashboard subtitle: Admin panel
    
admin.site.site_header = "Dj Afro"
admin.site.site_title = "Dj Afro Admin Panel"
admin.site.index_title = "Welcome to Dj Afro Admin Panel"
