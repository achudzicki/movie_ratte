# Django Model Query

---
    Przykłady zapytań do bazy danych wykorzystując Django Model
---
```text
Dla celów demo, wykorzystamy nowo utworzony Model Book.
Wszystkie komendy możemy wykonać w interaktywnej konsoli Django manage.
```
```python
python manage.py shell
```

### Utworzenie pierwszej encji naszej Książki

```text
W naszej klasie nie ma konstruktora przyjmującego nasze 
parametry. Model Django pozwala tworzyć obiekty przekazując do konstruktora
kwargs z naszymi wartościami.

```
Tworzenie nowej książki w bazie danych przy pomocy metody save.
```python
from books.models import Book

# Na ten moment nie poszło jeszcze zapytanie do bazy danych, na razie utworzyliśmy tylko zmienną.
lord_of_the_rings = Book(title='Lord of the rings', release_date='2021-01-01', rating_average=8.9, vote_count=1245)

# Klasa Model (Django) posiada metodę save, więc nasza klasa Book dziedzicząca po tej klasie
# też posiada taką metodę. Metoda zapisze naszą książkę do bazy danych.
lord_of_the_rings.save()
```

### Pobieranie elementów danego modelu

Najpierw pobieranie wszystkich encji danego modelu.
```python
from books.models import Book

# W tym momencie nie poszło jeszcze zapytanie do bazy danych. 
# Jest to tylko 'przepis' naszego zapytania.
get_all_books = Book.objects.all()

# Teraz dopiero poszło zapytanie do bazy danych.
print(get_all_books)
```

Pobieranie encji limitując wyniki (SQL LIMIT)
```python
from books.models import Book

# W tym momencie nie poszło jeszcze zapytanie do bazy danych. 
# Jest to tylko 'przepis' naszego zapytania.
# Zapytanie doda na końcu LIMIT 10 - mimo że składnia wydaje, się być
# zwykłą składnią Pythona (slice array)
get_all_books = Book.objects.all()[:10]

# Teraz dopiero poszło zapytanie do bazy danych.
print(get_all_books)
```

### Aktualizacja stanu encji (update)

```python
from books.models import Book

found_book = Book.objects.all()[0]
found_book.autor = 'JRR Tolkien'
# Django wie, że nie jest to nowa encja i zamiast zapisać nowy wiersz, zrobi update istniejącego.
# Funkcja save() działa na 2 sposoby. Tworzy nową encję lub robi update istniejącej.
found_book.save()
```

### Usuwanie danych

```python
from books.models import Book
found_book = Book.objects.all()[0]
found_book.delete()
```

### Dodawanie nowych encji 
Teraz dodamy nowe encje korzystając z metody create()

```python
from books.models import Book

# W metodzie crate przekazujemy nasze parametry jako kwargs
Book.objects.create(title='Lord of the rings', release_date='2021-01-01',
                    rating_average=8.9, vote_count=1245, author='JRR Tolkien')
Book.objects.create(title='Lord of the rings 2', release_date='2021-01-01',
                    rating_average=7.2, vote_count=987, author='JRR Tolkien')
Book.objects.create(title='Harry Potter', release_date='2020-01-01',
                    rating_average=8.1, vote_count=5874, author='J.K Rowling')
Book.objects.create(title='Alicja w Krainie Czarów', release_date='2021-01-01',
                    rating_average=5.9, vote_count=487, author='Lewis Carroll')
Book.objects.create(title='Nauka Django', release_date='2021-01-01',
                    rating_average=9.9, vote_count=1, author='Andrzej Chudzicki')
```

Zobaczmy też metodę zoptymalizowaną pod kątem tworzenia dużej ilości danych na raz.

```python
from books.models import Book

books = [
    Book(title='Lord of the rings', release_date='2021-01-01',
                        rating_average=8.9, vote_count=1245, author='JRR Tolkien'),
    Book(title='Lord of the rings 2', release_date='2021-01-01',
                        rating_average=7.2, vote_count=987, author='JRR Tolkien'),
    Book(title='Harry Potter', release_date='2020-01-01',
                        rating_average=8.1, vote_count=5874, author='J.K Rowling'),
    Book(title='Alicja w Krainie Czarów', release_date='2021-01-01',
                        rating_average=5.9, vote_count=487, author='Lewis Carroll'),
    Book(title='Nauka Django', release_date='2021-01-01',
                        rating_average=9.9, vote_count=1, author='Andrzej Chudzicki'),
]

# Przekazujemy tabelę z naszymi książkami.
Book.objects.bulk_create(books)
```

### Pobieranie encji przy pomocy metody get

Metoda get pobierze dokładnie 1 wynik po zadanych parametrach filtrowania.
Jeżeli znajdzie więcej niż 1 wynik dla podanych danych, rzuci błędem.
Jest to metoda przydatna, kiedy chcemy otrzymać dokładnie 1 wynik.
```python
from books.models import Book

# Truncate table and insert data to be sure we have id 1.
found_book = Book.objects.get(id=1)
```

### Filtrowanie wyników zapytania
Filtrowanie można wykorzystać zamiast metody get (i być zabezpieczonym przed błędem).

```python
from books.models import Book

found_book = Book.objects.filter(id=1)[0]

# Filtrowanie po Autorze
author = Book.objects.filter(author='JRR Tolkien')

# Filtrowanie po średniej głosów większej od 8.
Book.objects.filter(rating_average>8) # SKŁADNIA NIEDOZWOLONA!! Tutaj można tylko znak =

# Specjalna składnia dla operatorów >, <, >=, <=, like itp.
# Książki ze średnią większą od 8
average_vote = Book.objects.filter(rating_average__gt=8)

# Książki o nazwie LIKE 'lord'
title_like = Book.objects.filter(title__contains='lord')

# Książki ze średnią większą od 8 I nazwą LIKE 'lord'
title_like_and_average = Book.objects.filter(title__contains='lord', rating_average__gt=8)
```
**Należy zauważyć, że wszystkie warunki połączone są operatorem logicznym AND**
W celu połączenia zapytania operatorem OR, należy użyć specjalnej klasy Q().
```python
from books.models import Book
from django.db.models import Q

# Książki ze średnią większą od 8 LUB nazwą LIKE 'lord'
title_like_and_average = Book.objects.filter(Q(title__contains='lord') | Q(rating_average__gt=8))


# Książki ze średnią większą od 8 LUB nazwą LIKE 'lord' I autorem JRR Tolkien.
# Jeżeli chemy połączyć nasze filtry AND, wystarczy podać je po przecinku.
title_like_and_average = Book.objects.filter(Q(title__contains='lord') | Q(rating_average__gt=8),
                                             Q(author='JRR Tolkien'))
```

### Agregowanie i sortowanie

```python
from books.models import Book
from django.db.models import  Avg, Min, Max

all_books = Book.objects.all()

# Podczas wszystkich tych operacji poleci tylko 1 zapytanie do bazy (bo Django robi sobie cache).
# To jest optymalniejsze podejście.
num_of_books = all_books.count()
books_aggregate_info = all_books.aggregate(Avg("rating_average"), Min("rating_average"), Max("rating_average"))

print(f"Number of books: {num_of_books}")
print(f"Aggregation data: {books_aggregate_info}")

ordered = all_books.order_by("title")
print(ordered)

ordered = all_books.order_by("-title")
print(ordered)
```
