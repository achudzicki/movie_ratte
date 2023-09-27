# Aplikacja movies

---
Faza 1 (Views + Templates)
---

- Korzystamy z pliku [movies_small.csv](migrations/movies_small.csv)
- Dodajmy 1 endpoint dla [wszystkich filmów](views.py), tworząc nową klasę Movie
- Dodajemy 1 HTML z prostą tabelą [instrukcja tworzenia template](#praca-z-szablonami-widoków-templates)
  wykorzystując [Django Template Language](https://docs.djangoproject.com/en/4.2/ref/templates/language/)
- Zwracamy wszystkie filmy
- [Zadanie dla państwa](#zadanie-1)
- Dodanie do widoku wszystkich filmów możliwości przejścia do detali
  filmu. [Dynamiczny URL](https://docs.djangoproject.com/en/4.2/ref/templates/builtins/#url)
- Dodanie do widoku pojedynczego filmu poprawnego tekstu informującego, że dany film nie został znaleziony.
- Dodanie [dziedziczenia dokumentów HTML](#dziedziczenie-szablonów)
- Dodanie [plików statycznych](#dodanie-plików-statycznych)
- Stylowanie naszej tabeli i pojedynczego filmu
- Dodanie side-bar dla naszej aplikacji
- Wyodrębnimy nasze przyciski menu do osobnego HTML, poznając tag 'include'

---
Faza 2 (Django Model)
---

- [Dodanie obsługi bazy danych dla naszego modelu Movie](#dodanie-modelu-django). Dodanie dodatkowych pól w modelu
- Upewniamy się, że nasza aplikacja jest zarejestrowane w INSTALLED_APPS
- Ustawiamy [migrację](#dodanie-integracji-z-mssql-server), aby nasza tabela została wygenerowana
- Sprawdzamy, czy nasze filmy zostały zaimportowane do bazy danych
- Teraz proszę wykonać [Zadanie tworzenia migracji](../tworzenie_migracji.md)
- [Demo Django Query](../django_model_query.md)
- Przepisujemy metodę ['find_all'](#wyszukiwanie-wyników) aby korzystała ona z Django Models (ze względu na dużą ilość
  danych zaczytujemy pierwsze 50 wierszy)
- Przepisujemy metodę 'find_by_tmdb_id', aby korzystała ona z metody 'filter' Django Models
- Dodanie [walidatorów](https://docs.djangoproject.com/en/4.2/ref/validators/) dla naszych pól
- Dodanie prostego widoku prezentującego Query Params
- [Zadanie 2](#zadanie-2)
- Dodamy naszą stronę dla 404 i obsłużymy GET movie by ID

---
Faza 3 (Relations)
--- 

- Rozdzielenie naszej klasy Movie na mniejsze pod komponenty i powiązanie [jeden-do-jeden](#relacjaa-jeden-do-jeden)
- [Zadanie 3](#zadanie-3)
- [Demo Query powiązanych modeli](../django_model_query_relations.md)
- Sprawdzenie jak teraz wygląda panel admina i jak zarządzać tam relacjami
- Dodanie nowej klasy 'moja kolekcja filmów' i 'user' [powiązanie relacją jeden do wieli](#relacja-jeden-wiele)
- Wykonanie migracji bazy danych
- Dodanie powiązania relacją wiele do wielu, kolekcji filmów z filmami
- Wykonanie migracji bazy danych
- Poprawiamy nasze widoki: Wszystkich filmów, Szczegóły Filmu, aby były zgodne z nowym modelem
- [Zadanie 4](#zadanie-4)

---
Faza 4 (Forms)
---

- Dodanie [formularza](#praca-z-formularzami-dodawania-danych) dodawania nowych filmów w znany sposób HTML+POST
- Dodanie panelu nawigacyjnego dla admina
- Dodanie klasy MovieForm jako Django Form [forms.py](forms.py)
- Dodanie walidacji dla naszych pól klasy MovieForm
    - Required
    - Max Length
    - Data wydania musi być w przeszłości
- Dodanie walidacji (logiki biznesowej) podczas dodawania filmu:
    - Jeżeli film o danym tytule już istnieje, to nie można dodać filmu
- Dodanie naszego formularza jako ModelForm
- Dodanie paginacji na stronie z filmami (5 filmów)
- Dodanie nowych stylów na stronie z filmami
- Dodanie integracji z IMDB API
- Dodanie wyszukiwania po nazwie filmu
- Dodanie nowych stylów dla szczegółów filmu
- Dodanie na stronie szczegółów filmu 5 najnowszych filmów
- Poprawienie stylu strony z dodawaniem Filmu
- [Zadanie 5](#zadanie-5)

## Praca z szablonami widoków (templates)

### Tworzenie nowego folderu dla Templates

- Utworzenie folderu templates w odpowiedniej aplikacji django
- W utworzonym folderze dodanie kolejnego folderu z nazwą **taką samą jak nazwa aplikacji**

```text
   Po powyższych krokach możemy spróbować wywołać nasz URL - ale zauważymy tam błąd.
```

- Rejestrujemy nasz folder templates w pliku [settings.py](../moverrate/settings.py)

```text
   Szukamy w ustawieniach ustawień 'TEMPLATES' i interesujące nasz opcje to:
   
   - DIRS
   - APP_DIRS
   
   Widzimy także w ustawieniach zmienną o nazwie BASE_DIR, ustawia ona główną absolutną 
   ścieżkę naszej aplikacji i to od niej będziemy podawali ścieżki do naszych folderów
   i innych zasobów
```

- Dodajemy w DIRS ścieżkę do naszych templates w aplikacji movies

```python
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'movies' / 'templates'
        ]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Inną opcją dodania rozpoznawania folderów np. z templates przez Django jest skorzystanie z
APP_DIRS. Domyślnie ustawione na true oznacza to, że Django automatycznie będzie szukało
folderów templates w naszej aplikacji, **Jednak się to nie dzieje**.
**Aby móc skorzystać z tej opcji, musimy [zarejestrować](#rejestrowanie-aplikacji-w-django) naszą aplikację, tak aby
Django wiedziało o jej istnieniu.**

### Rejestrowanie aplikacji w Django

- Dodanie odpowiedniej aplikacji **po jej nazwie**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'movies'
]
```

### Zwracanie HTML z widoków

Aby móc zwrócić HTML z naszego widoku potrzebujemy przekształcić cały wygenerowany kontent
w String i zwrócić go w naszym HttpResponse. W tym celu należy zaimportować metodę:

```python
from django.template.loader import render_to_string
```

I zwrócić nasz przetworzony plik HTML

```python
from django.shortcuts import HttpResponse
from django.template.loader import render_to_string


def get_data(request):
    return HttpResponse(render_to_string('movies/movies.html'))
```

Można także użyć skrótu, który zawiera w sobie i HttpResponse i render_to_string -> render.
Przy wykorzystaniu skrótu render(), musimy przekazać do niego także obiekt request.

```python
from django.shortcuts import render


def all_movies(request):
    return render(request, 'movies/movies.html')
```

### Django Template Language

https://docs.djangoproject.com/en/4.2/ref/templates/language/

```text
"Język szablonów Django został zaprojektowany tak, aby zapewnić równowagę pomiędzy mocą i łatwością.
Został zaprojektowany tak, aby był wygodny dla osób przyzwyczajonych do pracy z HTML.
Jeśli masz kontakt z innymi językami szablonów tekstowych, takimi jak Smarty lub Jinja2, 
powinieneś czuć się jak w domu dzięki szablonom Django."
```

**Używając składni {{ <zmienna> }} nie możemy zawrzeć tam kodu Pythona. Z pomocą prostych operacji przychodzą nam
filtry.**
Mając doświadczenie z Jinja2 podczas pracy z Flask, będzie nam się łatwo przestawić na
używanie Django Template Language (DTL). Poza standardowymi rzeczami, które widzieliśmy już
korzystając z Jinja Django
posiada [Filtry](https://docs.djangoproject.com/en/4.2/ref/templates/builtins/#built-in-filter-reference)

### Dziedziczenie szablonów

Aby zapobiegać duplikowaniu kodu w szablonach HTML, możemy wprowadzić dziedziczenie szablonów.

- Najpierw tworzymy nowy folder w [głównym folderze naszego projektu](../templates). (Przy tworzeniu projektu PyCharm
  wygenerował go za nas)
- Tworzymy nowy dokument HTML o nazwie [base.html](../templates/base.html), będzie to główny layout naszego programu
- Dodajemy do niego 2 dynamiczne sekcje: Tytuł i Body. Do tego użyjemy taga 'block' (podobnie jak we Flask)

```html
{% block
<nazwa-blooku>%}
    <domyślna-wartość-gdy-nie-przekazane-nic/>
    {% endblock %}
```

 ```html
  <title>{% block page_title%}Domyślny tutuł jak nie podamy nic{% endblock %}</title>
```

 ```html

<body>
{% block page_content%}
{% endblock %}
</body>
``` 

- Poinformowanie Django o ścieżce do naszego głównego HTML w pliku [settings.py](../moverrate/settings.py). Dodajemy w
  ustawieniach TEMPLATES odpowiednią ścieżkę.

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

- Dziedziczymy w naszych dokumentach HTML z właśnie utworzonego **base.html**. Wykorzystamy tag 'extends'. Dodajemy w
  odpowiednich blokach, nazwę strony i body.

```html
{% extends 'base.html' %}
```

- Dziedziczenie może być kontynuowane w kolejnych plikach.

```text
 base.html -> movies.html -> other.html
```

### Dodanie plików statycznych

Dodamy stylowanie UiKit (css, js) do folderu [static](../static) w głównym folderze.
Aby pliki statyczne działały, trzeba się upewnić, że w pliku [settings.py](../moverrate/settings.py)
w sekcji INSTALLED_APPS mamy:

```text
    'django.contrib.staticfiles'
```

Pliki statyczne można także dodawać na poziomie aplikacji, podobnie do templates.

- W pliku [base.html](../templates/base.html) dodajemy nowy tag

```html
{% load static %}
```

- Dodajemy ścieżki do naszych plików css i js przy pomocy nowego taga 'static'

```html

<link rel="stylesheet" href="/static/css/uikit.min.css">

<script src="/static/js/uikit.min.js"></script>
<script src="/static/js/uikit-icons.min.js"></script>
```

- Domyślnie Django szuka plików statycznych **tylko w aplikacjach**, aby dodać globalne pliki statyczne, potrzebne są
  dodatkowe kroki.
- W pliku konfiguracyjnym [settings.py](../moverrate/settings.py) dodajmy nową listę STATICFILES_DIRS

```python

```

## Praca z bazą danych

### Dodanie Modelu Django

https://docs.djangoproject.com/en/4.2/ref/models/fields/#field-types

- Aby dany Model był traktowany jako obiekt, który zostanie zmapowany na encję bazodanową musi dziedziczyć po klasie
  Model

```python
from django.db import models


class Movie(models.Model):
    pass
```

- Następnie musimy zdefiniować wszystkie pola naszej klasy, które będą mapowane na kolumny w relacyjnej bazie danych

```python
from django.db import models


class Movie(models.Model):
    id = models.AutoField()
    tmdb_id = models.IntegerField(),
    original_language = models.CharField(max_length=10),
    original_title = models.CharField(max_length=512)
    overview = models.TextField()
    popularity = models.DecimalField(max_digits=10, decimal_places=2)
    release_date = models.DateField()
    title = models.CharField(max_length=512)
    vote_average = models.DecimalField(max_digits=2, decimal_places=1)
    vote_count = models.IntegerField()
```

```text
Należy pamiętać że pole ID nie musi być zdefiniowane. Django automatycznie doda auto-generowane ID dla naszych
modeli. Niektóre z typów wymagają jednego lub więcej argumentów, np. DecimalField czy CharField
```

### Dodanie integracji z MsSql Server

- Instalujemy pakiet mssql-django

```bash
python -m pip install django mssql-django
```

- W pliku [settings.py](../moverrate/settings.py) ustawiamy dane dla naszej bazy danych

```python
DATABASES = {
    'default': {
        "ENGINE": "mssql",
        "NAME": "chudzick",
        "USER": "chudzick",
        "PASSWORD": "Maslow180!",
        "HOST": "morfeusz.wszib.edu.pl",
        "PORT": "1433",
        "OPTIONS": {
            "driver": "ODBC Driver 18 for SQL Server",
            'extra_params': 'Encrypt=no',
        },
    }
}
```

- W pierwszym kroku wykonujemy polecenie z linii komend. Nawigujemy się do folderu projektu, nie aplikacji!
- W naszym przypadku możemy też wywołać to w PyCharm Tools > Run manage tasks > komenda

```bash
python manage.py makemigrations
```

- Wygenerowana została pierwsza migracja w naszej aplikacji movies
- Dodajemy teraz ładowanie
  naszych [danych wejściowych](migrations/movies.csv). https://docs.djangoproject.com/en/4.2/topics/migrations/#data-migrations
- Dodajemy właśnie napisaną metodę do operations, aby wykonała się po utworzeniu nowej tabeli Movies.

```python
from movies.models import Movie
import csv
import datetime


def load_initial_data(apps, schema_editor):
    movies_arr = []
    with open('movies/migrations/movies.csv', 'r', encoding='utf-8') as all_movies_file:
        all_movies_file.readline()
        reader = csv.reader(all_movies_file, delimiter=',')

        for row in reader:
            movie = Movie(tmdb_id=row[1], original_title=row[5], overview=row[11], popularity=float(row[2]),
                          release_date=datetime.datetime.strptime(row[15], '%m/%d/%Y'), vote_average=float(row[17]),
                          vote_count=int(row[16]), cast=row[6], genres=row[13], director=row[8], keywords=row[10])
            movies_arr.append(movie)

        Movie.objects.bulk_create(movies_arr)
```

- Uruchamiamy właściwą migrację, tworzymy tabele i insertujemy dane wejściowe

```bash
python manage.py migrate
```

- Migracja została uruchomiona i możemy zobaczyć wygenerowane tabele oraz dodane rekordy do tabeli movies

```text
Django wygenerowało więcej tabel niż się spodziewaliśmy. Powodem tego jest to że 
w INSTALLED_APPS mamy więcej aplikacji (np. Admin) i one też potrzebują tabel do działania.
```

### Wyszukiwanie wyników

#### all()

Przepiszemy naszą metodę 'find_all' aby korzystała ona z Django Models.
Dzięki temu, że nasza klasa Movie dziedziczy po klasie Model, ma ona dostęp do pola 'objects'.
Pole object ma dostęp do wielu metod potrzebnych do interakcji z bazą danych.
W celu wyciągnięcia wszystkich wyników z bazy danych dla danego modelu możemy zastosować:

```python
from movies.models import Movie

Movie.objects.all()
```

Ze względu na to, że w naszej tabeli movies jest blisko 10K rekordów, na początek chcemy zwrócić jedynie pierwsze
50 wyników, w tym celu musimy zastosować limit.

```python
from movies.models import Movie

Movie.objects.all()[:50]
```

Na pierwszy rzut oka wydawałoby się, żę najpierw zaczytamy wszystkie dane, a później dopiero zrobimy slice naszych
wyników.
Zestawy zapytań Django są leniwe. Oznacza to, że zapytanie trafi do bazy danych tylko wtedy, gdy wyraźnie poprosisz o
wynik.
Więc w naszym przypadku Django wygeneruje poprawne zapytanie z częścią "LIMIT 50"

#### get()

Aby otrzymać **dokładnie jeden** wynik, możemy użyć metody get() i przekazać do niej nasze 'filtry'

```python
from movies.models import Movie

Movie.objects.get()

Movie.objects.get(tmdb_id='TT11111')
```

Należy pamiętać, że jeżeli nie jesteśmy pewni tego, że w rezultacie otrzymamy 1 wynik, to nie należy używać
get. Znajdując więcej niż 1 wynik, metoda .get() rzuci nam błędem. Jeżeli nie jesteśmy pewni, że w wyniku otrzymamy
dokładnie jeden wynik, lepiej jest zastosować metodę .filter()

#### filter()

Metoda filter pozwala nam na filtrowanie danych zwrotnych z bazy danych.
Należy pamiętać, że chcąc filtrować pola np. liczbowe, nie możemy porównywać ich
logicznymi operatorami takimi jak '<', '>', '<=' ... Zamiast tego musimy użyć [specjalnej składni dostarczonej przez
Django](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#field-lookups)

```python
from movies.models import Movie

# Zwrócenia danych wszystkich
Movie.objects.filter(tmdb_id='test111')

# Zwrócenie tylko 1 znalezionej wartości
Movie.objects.filter(tmdb_id='test111').first()

# Zwrócenie danych większych niż
# używamy specjalnej składni. Po nazwie naszego pola __gt
# Django posiada cały zestaw operatorów https://docs.djangoproject.com/en/4.2/ref/models/querysets/#field-lookups
# Zwróć filmy gdzie liczba głosów > 10 I średnia < 7.5
Movie.objects.filter(vote_count__gt=10, vote_average__lt=7.5)
```

Metoda 'filter' napisany w ten sposób łączy nasze warunki operatorem logicznym AND. Gdy chcemy połączyć nasze warunki
operatorem OR, musimy użyć specjalnej klasy dostarczonej przez Django Q.

```python
from movies.models import Movie
from django.db.models import Q

# Zwróć filmy gdzie liczba głosów > 10 LUB średnia < 7.5
Movie.objects.filter(Q(vote_count__gt=10) | Q(vote_average__lt=7.5))

# Jeżeli chcemy dodać kolejny warunek i połączyć AND to podajemy go po przecinku
# Zwróć filmy gdzie (liczba głosów > 10 LUB średnia < 7.5) I reżyser = 'Test Director'
Movie.objects.filter(Q(vote_count__gt=10) | Q(vote_average__lt=7.5), Q(director='Test Director'))
```

### Definiowanie Relacji pomiędzy obiektami

#### Relacja jeden do jeden

Rozbijemy sobie naszą klasę Movie na mniejsze pod komponenty, wyodrębnimy nową klasę Movie statistics.
Powiążemy nasze klasy relacją 1-1 używając **OneToOneField**

```python
from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator
from django.db import models


class MovieStatistics(models.Model):
    vote_average = models.DecimalField(max_digits=5, decimal_places=2,
                                       validators=[MinValueValidator(1)])
    vote_count = models.IntegerField()
    popularity = models.DecimalField(max_digits=20, decimal_places=10)


class Movie(models.Model):
    tmdb_id = models.CharField(max_length=255)
    original_title = models.CharField(max_length=1000)
    overview = models.TextField()
    release_date = models.DateField()
    cast = models.CharField(max_length=1000)
    genres = models.CharField(max_length=1000)
    director = models.CharField(max_length=1000)
    keywords = models.TextField(validators=[MinLengthValidator(10)])
    # Tak też można
    # statistics = models.ForeignKey(MovieStatistics, on_delete=models.CASCADE)
    statistics = models.OneToOneField(MovieStatistics, on_delete=models.CASCADE, primary_key=True)
```

Powiązanie klasy 1-1:

- Dodajemy pole ForeignKey
- W konstruktorze podajemy nazwę klasy, z którą chcemy połączyć naszą encję
- Dodajemy Name parameter 'on_delete', czyli informację co ma się stać z naszą encją po usunięciu obiekty Movie
- Ustawiamy CASCADE, czyli nasza encja MovieStatistic zostanie usunięta w momencie usuwania Movie

#### Relacja jeden-wiele

Podobnie jak relacja jeden do jeden ale używamy **ForeginKey**

## Praca z formularzami dodawania danych

### Django Forms

Django pomaga nam przy walidacji naszych formularzy w sposób wygodny.

- Dodajemy w naszej aplikacji plik [forms.py](forms.py). Jest to opcjonalne, jednak często dodaje się taki dodatkowy
  plik dla czytelności.
-

# Zadania

## Zadanie 1

```text
Proszę napisać nowy endpoint który przy pomocy tmdb_id będzie wyszukiwał dany film i prezentował dane
w nowym widoku 
```

---

1) Dodanie nowego wpisu w pliku views.py
2) Dodanie mapowania URL w urls.py
3) Dodanie nowego pliku HTML w folderze static/movies
4) Dodanie nowej metody w klasie Movies, get_by_tmdb_id
5) Zaprezentowanie nowego widoku pod url /movies/<int:tmdb_id>

<span style="color:yellow">Czas na wykonanie zadania - 20min.</span>

## Zadanie 2

```text
Proszę napisać nowy endpoint który będzie umożliwiał filtrowanie naszych filmów po tytule 'ILIKE'. 
Filtrując proszę użyć metody __contains z Django models.
```

1) Dodanie nowego mapowania URL w urls.py (nie korzystamy z istniejącego URL /movies)
2) Dodanie nowej metody w views.py
3) Zwrócenie widoku
4) Przetestowania działania ręcznie tworząc URL w przeglądarce

<span style="color:yellow">Czas na wykonanie zadania - 20min.</span>

## Zadanie 3

```text
Proszę przepisać klasę Book i wyodrębnić z niej Autora. 
Proszę połączyć klasy relacją jeden do jeden
```

1) Dodać nową klasę Autor
    - first_name
    - last_name
2) Połączyć klasę Book z klasą Author relacją jeden do jeden
3) Utworzyć nową migrację
4) Korzystając z CMD dodać nową książkę wraz z powiązanym autorem

<span style="color:yellow">Czas na wykonanie zadania - 15min.</span>

## Zadanie 4

```text
Proszę dopisać nowy widok dla kolekcji filmów. (Analogicznie jak Filmy i szczegóły filmów)
```

1) Dodać nowy url dla wszystkich kolekcji filmów i szczegółów kolekcji
2) Dodać nowy widok dla kolekcji filmów i szczegółów kolekcji
3) Dodać nowe HTML dla obu widoków
4) Dodać link w menu dla Listy Kolekcji Filmów
5) Dodać ręcznie kilka danych testowych (kolekcja filmów, user). Preferowana forma dodania przez konsole.

<span style="color:yellow">Czas na wykonanie zadania - 45min.</span>

## Zadanie 5 (Wykonane wspólnie)

```text
Proszę dodać formularz dodawania kolekcji filmów.
```

1) Dodać nowy formularz w klasie [forms.py](forms.py). Sposób dowolny ModelForm/Form.
2) Dopisać dla istniejącego widoku logikę zapisywania nowej kolekcji filmów

<span style="color:yellow">Czas na wykonanie zadania - 20min.</span>

## Zadanie 6 
```text
Proszę dodać funkcjonalność dodawania filmów do kolekcji. Dodawanie filmu powinno odbywać się z poziomu
szczegółów filmu. Powinniśmy móc dodać film tylko do kolekcji w których go jeszcze nie ma.
Po kliknięciu w guzik dodawania do kolekcji przenosimy użytkownika do nowej strony z wyborem kolekcji.
```