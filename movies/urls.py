from django.urls import path
from .views import home, MovieList, MovieDetail,watch_trailer, checkout, watchlist

urlpatterns = [
    path('', home, name='home'),
    path('movies/', MovieList.as_view(), name='movie-list'), 
    path('movies/<uuid:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('movie/<uuid:movie_id>/watch-trailer/', watch_trailer, name='watch-trailer'),
    path('movie/<uuid:movie_id>/checkout/', checkout, name='checkout'),
    path('watchlist/', watchlist, name='watchlist'),
]


