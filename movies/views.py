from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView
from django.views import View
from django.db.models import Q, Avg
from .models import Movie, Person, Genre
from comments.models import Comment
from likes.models import Like
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# home
def home(request):
    movies = Movie.objects.all()
    celebrities = Person.objects.all()

    # Annotate each movie with its average rating
    movies_with_ratings = movies.annotate(avg_rating=Avg('ratings__rating'))

    # Extract the ratings from the annotated movies
    ratings = [movie.avg_rating or 0 for movie in movies_with_ratings]

    # Calculate the number of likes and comments for each movie
    movie_likes = {movie.id: Like.objects.filter(movie=movie).count() for movie in movies}
    movie_comments = {movie.id: Comment.objects.filter(movie=movie).count() for movie in movies}

    # Sort movies based on likes and get popular movies
    popular_movies = sorted(movies, key=lambda x: movie_likes.get(x.id, 0), reverse=True)[:10]

    genres = Genre.objects.all()

    context = {
        'celebrities': celebrities,
        'movies': movies,
        'slider_movies': movies.filter(to_slider=True),
        'latest_movies': movies.order_by('-release_date')[:10],
        'popular_movies': popular_movies,
        'ratings': ratings,
        'likes': movie_likes,
        'comments': movie_comments,
        'genres': genres,
    }
    return render(request, 'home.html', context)

class MovieList(ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 10  # Adjust as needed

    def get_queryset(self):
        query = self.request.GET.get('q')
        filter_by_genre = self.request.GET.get('filter_by_genre')

        if query:
            movies = Movie.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        else:
            movies = Movie.objects.all()

        if filter_by_genre:
            movies = movies.filter(genre__id=filter_by_genre)

        return movies

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['filter_by_genre'] = self.request.GET.get('filter_by_genre', '')
        context['genres'] = Genre.objects.all()
        return context

class MovieDetail(View):
    model = Movie
    template_name = 'movies/movie_detail.html'

    def get(self, request, *args, **kwargs):
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        comments = Comment.objects.filter(movie=movie).order_by('-created_at')
        likes = Like.objects.filter(movie=movie).count()

        context = {
            'object': movie,
            'comments': comments,
            'likes': likes,
        }

        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        action = request.POST.get('action')

        # Handle comment submission
        if action == 'comment' and 'comment_text' in request.POST:
            comment_text = request.POST['comment_text']
            Comment.objects.create(user=request.user, movie=movie, text=comment_text)

        # Handle like submission
        elif action == 'like':
            self.like_movie(request.user, movie)

        return redirect('movie-detail', pk=self.kwargs['pk'])

    def like_movie(self, user, movie):
        # Check if the user has already liked the movie
        existing_like = Like.objects.filter(user=user, movie=movie).exists()

        if not existing_like:
            # If the user hasn't liked the movie, create a new Like instance
            Like.objects.create(user=user, movie=movie)


# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib import messages
from .models import Movie, Transaction, UserProfile

@login_required
def watch_trailer(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    return render(request, 'watch_trailer.html', {'movie': movie})

login_required
def checkout(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # Check if the movie is already in the user's watchlist
    user_profile = UserProfile.objects.get(user=request.user)
    if movie in user_profile.watchlist.all():
        messages.warning(request, "This movie is already in your watchlist.")
    else:
        # Assuming your Movie model has a field named "price"
        amount = movie.price

        # Add movie to user watchlist
        user_profile.watchlist.add(movie)

        # Create a new transaction with the specified amount
        Transaction.objects.create(user=request.user, movie=movie, amount=amount)

        messages.success(request, "Movie added to your watchlist successfully.")

    # Redirect to the user's watchlist or another appropriate page
    return HttpResponseRedirect(reverse('watchlist'))

@login_required
def watchlist(request):
    user_profile = UserProfile.objects.get(user=request.user)
    watchlist_items = user_profile.watchlist.all()
    return render(request, 'movies/watchlist.html', {'watchlist_items': watchlist_items})