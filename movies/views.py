from django.shortcuts import render, get_object_or_404

from . import models


def all_movies(request):
    # Pobieramy jedynie 50 wyników, tutaj zadziała lazy.
    movies_array = models.Movie.objects.all()[:50]
    return render(request, 'movies/movies.html', {
        "movies": movies_array
    })


def filter_movies(request):
    title = request.GET.get('title')
    if title:
        found_movies = models.Movie.objects.filter(original_title__contains=title)
    else:
        found_movies = models.Movie.objects.all()[:50]

    return render(request, 'movies/movies.html', {
        "movies": found_movies,
        "filter_name": title
    })


def find_by_tmdb_id(request, id):
    # To będzie to samo
    # models.Movie.objects.filter(tmdb_id=tmdb_id).first()
    # models.Movie.objects.get(tmdb_id=tmdb_id)

    # .get() pobierze 1 wynik pasujący do naszych key = value i get zawsze zwróci tylko 1 wynik.
    # Znajdując więcej niż 1 wynik, rzuci nam błędem.
    # Używać mając pewność, że jest unikalna wartość w bazie
    # Dla pewności można używać filter() -> zadziała podobnie ale zwróci więcej wartości.
    # Porównywanie nie może odbyć się przez operatory logiczne <, > itp.
    # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#field-lookups

    # Tutaj dodatkowo skrót metoda, jak nie znajdzie obiektu, to rzuci 404.
    # Dodając plik HTML 404.html i ustawiając wartość DEBU = false w pliku settings.py,
    # Django automatycznie wyświetli nam nasz template 404.
    # Na razie tego nie zrobimy, bo będziemy musieli ustawić ALLOWED_HOSTS[].
    found_movie = get_object_or_404(models.Movie, id=id)
    return render(request, 'movies/movie.html', {
        "movie": found_movie
    })
