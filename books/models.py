from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    rating_average = models.DecimalField(
        max_digits=3, decimal_places=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    vote_count = models.IntegerField()
    author = models.CharField(max_length=255, default=None, null=True)

    def __str__(self):
        return f"{self.title}"
