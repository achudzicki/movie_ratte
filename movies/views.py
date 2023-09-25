from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

from .forms import MovieForm
from .models import Movie, MovieCollection, MovieStatistics


def all_movies(request):
    movies_array = Movie.objects.all()[:50]
    return render(request, 'movies/movies.html', {
        "movies": movies_array
    })


def add_movie(request):
    if request.method == 'POST':
        # Wyciągamy dane z naszego formularza
        new_movie_data = request.POST
        initial_statistics = MovieStatistics.objects.create(vote_average=0, vote_count=0, popularity=0)
        movie = Movie.create_from_form(new_movie_data)
        movie.statistics = initial_statistics
        movie.save()

        # W redirect podajemy name naszego widoku (ustawiany w pliku urls.py)
        return redirect('all_movies')

    if request.method == 'GET':
        form = MovieForm()

    return render(request, 'movies/admin/movie_add.html', {
        'movie_form': form
    })


def filter_movies(request):
    title = request.GET.get('title')
    if title:
        found_movies = Movie.objects.filter(original_title__contains=title)
    else:
        found_movies = Movie.objects.all()[:50]

    return render(request, 'movies/movies.html', {
        "movies": found_movies,
        "filter_name": title
    })


def find_by_tmdb_id(request, id):
    found_movie = get_object_or_404(Movie, id=id)
    return render(request, 'movies/movie.html', {
        "movie": found_movie
    })


def all_collections(request):
    movie_collections = MovieCollection.objects.all().annotate(movie_count=Count('movies'))
    return render(request, 'movies/movies_collection.html', {
        "collections": movie_collections
    })


def collection_details(request, id):
    movie_collection = MovieCollection.objects.get(pk=id)
    movies_in_collection = movie_collection.movies.all()
    return render(request, 'movies/collection_details.html', {
        'collection': movie_collection,
        'movies': movies_in_collection
    })
