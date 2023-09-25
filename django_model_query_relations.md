# Django Model Query

---

    Przykłady zapytań do bazy danych wykorzystując Django Powiązanych Model

---

```text
Zauważmy że ocena filmu znajduje się w osobnej klasie która jest powiązana
relacją jeden do jeden z klasą filmu.
```

```python
from movies.models import Movie, MovieStatistics

# Wszystkie filmy, które mają średnią ocenę większą od 9
Movie.objects.filter(statistics__vote_average__gt=9)

# Wszystkie filmy, które mają liczbę głosów większą od 2000 I mniejszą od 2200
Movie.objects.filter(statistics__vote_count__gt=2000, statistics__vote_count__lt=2200)
```

Składnia podobna do poprzednich filtrowań, można filtrować po połączonym modelu.
<nazwa-połączonego-modelu>__<nazwa-pola-modelu>__<operator_logiczny>

Query modelu filmu od strony Statystyk. W tym celu należy użyć specjalnej składni __set

```python
from movies.models import Movie, MovieStatistics

statistics_vote_over_8 = MovieStatistics.objects.filter(vote_average__gt=8)
# Dostajemy tutaj reverse obiekty
movies_from_statistics = statistics_vote_over_8.movie_set
# Tutaj dostajemy dopiero obiekty filmów
movies_from_statistics.all()
# Możemy też filtrować na tym obiekcie dalej 
movies_from_statistics.filter(orginal_title__contains='lord')
```

## Dla many to many trzeba użyć metod **add() lub set()**