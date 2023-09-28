import datetime

from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import MovieForm, MovieCollectionForm
from .models import Movie, MovieCollection, User


@login_required
def all_movies(request):
    # Pamiętamy, że tutaj nie idzie jeszcze zapytanie do bazy danych
    title = request.GET.get('title')
    if title:
        movies = Movie.objects.filter(original_title__contains=title)
    else:
        movies = Movie.objects.all()

    # Tworzymy instancje Paginatora
    paginator = Paginator(movies, 5)

    # Patrzymy, o jaką stronę nam chodzi (podajemy query param 'page').
    page_num = request.GET.get('page', 1)

    # Finalnie tworzymy obiekt Strony z naszymi Danymi
    page = paginator.get_page(page_num)

    # print(page.object_list)
    # print(page.number)
    # print(page.has_previous())
    # print(page.has_next())
    # if page.has_previous():
    #    print(page.previous_page_number())
    # if page.has_next():
    #    print(page.next_page_number())

    return render(request, 'movies/movies.html', {
        "movies_page": page,
        "filter_name": title
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_movie(request):
    if request.method == 'POST':
        # Wyciągamy dane z naszego formularza
        new_movie_data = MovieForm(request.POST)

        if new_movie_data.is_valid():
            movie_data = new_movie_data.cleaned_data

            if Movie.movie_with_tile_exist(movie_data['title']):
                return render(request, 'movies/admin/movie_add.html', {
                    'movie_form': new_movie_data,
                    'additional_errors': [f"Film o tytule {movie_data['title']} już istnieje"]
                })

            Movie.create_from_form(movie_data)
            # W redirect podajemy name naszego widoku (ustawiany w pliku urls.py)
            return redirect('all_movies')
    else:
        new_movie_data = MovieForm()

    return render(request, 'movies/admin/movie_add.html', {
        'movie_form': new_movie_data
    })


@login_required
def find_by_tmdb_id(request, id):
    found_movie = get_object_or_404(Movie, id=id)
    latest_movies = Movie.objects.all().order_by('-release_date')[:5]
    return render(request, 'movies/movie.html', {
        "movie": found_movie,
        "latest_movie": latest_movies
    })


@login_required
def movie_collections(request):
    additional_errors = []
    if request.POST:
        new_collection = MovieCollectionForm(request.POST)

        if new_collection.is_valid():
            collection_data = new_collection.cleaned_data

            if not MovieCollection.collection_exist(collection_data['name']):
                # Na razie bierzemy 1 ownera z góry, później będzie to zalogowana osoba.
                owner = User.objects.all()[:1][0]
                MovieCollection.objects.create(name=collection_data['name'], creation_date=datetime.date.today(),
                                               update_date=datetime.date.today(), owner=owner)
                return redirect('all_collections')

            additional_errors.append(f"Kolekcja o nazwie {collection_data['name']} już istnieje!")
    else:
        new_collection = MovieCollectionForm()

    found_collections = MovieCollection.objects.all().annotate(movie_count=Count('movies'))
    return render(request, 'movies/movies_collection.html', {
        "collections": found_collections,
        'collection_form': new_collection,
        'additional_errors': additional_errors
    })


@login_required
def collection_details(request, id):
    movie_collection = MovieCollection.objects.get(pk=id)
    movies_in_collection = movie_collection.movies.all()
    paginator = Paginator(movies_in_collection, 5)
    page = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'movies/collection_details.html', {
        'collection': movie_collection,
        'movies_page': page
    })


@login_required
def add_movie_to_collection(request, movie_id):
    found_movie = get_object_or_404(Movie, id=movie_id)

    if request.POST:
        collection = get_object_or_404(MovieCollection, id=request.POST.get('collection_id', 0))
        collection.update_date = datetime.date.today()
        collection.movies.add(found_movie)
        collection.save()
        return redirect('all_collections')

    available_collections = MovieCollection.objects.exclude(movies__id=movie_id)
    return render(request, 'movies/movie_collection_bind.html', {
        'movie': found_movie,
        'available_collections': available_collections
    })


@login_required
def remove_movie_from_collection(request, collection_id, movie_id):
    collection = get_object_or_404(MovieCollection, id=collection_id)
    movie_to_remove = get_object_or_404(Movie, id=movie_id)
    collection.movies.remove(movie_to_remove)
    return redirect('collection', id=collection_id)


@login_required
def remove_collection(request, collection_id):
    collection_to_remove = get_object_or_404(MovieCollection, id=collection_id)
    collection_to_remove.delete()
    return redirect('all_collections')
