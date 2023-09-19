from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator


# Create your models here.
class Movie(models.Model):
    tmdb_id = models.CharField(max_length=255)
    # CharField ma 1 argument wymagany 'max_length'
    original_title = models.CharField(max_length=1000)
    overview = models.TextField()
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/#decimalfield
    popularity = models.DecimalField(max_digits=20, decimal_places=10)
    release_date = models.DateField()
    vote_average = models.DecimalField(max_digits=5, decimal_places=2,
                                       validators=[MinValueValidator(1)])
    vote_count = models.IntegerField()
    cast = models.CharField(max_length=1000)
    genres = models.CharField(max_length=1000)
    director = models.CharField(max_length=1000)
    keywords = models.TextField(validators=[MinLengthValidator(10)])
