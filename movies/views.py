from django.shortcuts import render
from django.http import HttpResponseNotFound

from . import models


# Utworzenie 1 widoku z wszystkimi filmami

def all_movies(request):
    # Utworzymy sobie w naszych modelach klasę Movie.
    movies_array = models.Movie.get_all_movies()

    # Przekazujemy jako mapę, listę naszych danych wejściowych dla tempalte
    return render(request, 'movies/movies.html', {
        "movies": movies_array
    })
    # To jest skrót dla takiej składni
    # return HttpResponse(render_to_string('movies/movies.html'))


def find_by_tmdb_id(request, tmdb_id):
    found_movie = models.Movie.find_by_tmdb_id(tmdb_id)
    return render(request, 'movies/movie.html', {
        "movie": found_movie
    })
