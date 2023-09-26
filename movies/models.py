from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models


class MovieStatistics(models.Model):
    vote_average = models.DecimalField(max_digits=5, decimal_places=2,
                                       validators=[MinValueValidator(1)])
    vote_count = models.IntegerField()
    popularity = models.DecimalField(max_digits=20, decimal_places=10)


# Create your models here.
class Movie(models.Model):
    tmdb_id = models.CharField(max_length=255)
    original_title = models.CharField(max_length=1000)
    overview = models.TextField()
    release_date = models.DateField()
    cast = models.CharField(max_length=1000)
    genres = models.CharField(max_length=1000)
    director = models.CharField(max_length=1000)
    keywords = models.TextField(validators=[MinLengthValidator(10)])
    statistics = models.OneToOneField(MovieStatistics, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.original_title}"

    @staticmethod
    def movie_with_tile_exist(title: str):
        found_count = Movie.objects.filter(original_title=title).count()
        return found_count > 0

    @staticmethod
    def create_from_form(form_data):
        initial_statistics = MovieStatistics.objects.create(vote_average=0, vote_count=0, popularity=0)

        Movie.objects.create(
            tmdb_id=form_data['tmdb_id'],
            original_title=form_data['title'],
            overview=form_data['overview'],
            release_date=form_data['release_date'],
            cast=form_data['cast'],
            genres=form_data['genres'],
            director=form_data['director'],
            keywords=form_data['keywords'],
            statistics=initial_statistics
        )


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    birth_day = models.DateField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class MovieCollection(models.Model):
    name = models.CharField(max_length=255)
    creation_date = models.DateField()
    update_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie)
