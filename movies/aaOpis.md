# Aplikacja movies

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

---

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
{% block  <nazwa-blooku>%}
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
- Poinformowanie Django o ścieżce do naszego głównego HTML w pliku [settings.py](../moverrate/settings.py). Dodajemy w ustawieniach TEMPLATES odpowiednią ścieżkę.
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
- Dziedziczymy w naszych dokumentach HTML z właśnie utworzonego **base.html**. Wykorzystamy tag 'extends'. Dodajemy w odpowiednich blokach, nazwę strony i body.
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
- Domyślnie Django szuka plików statycznych **tylko w aplikacjach**, aby dodać globalne pliki statyczne, potrzebne są dodatkowe kroki.
- W pliku konfiguracyjnym [settings.py](../moverrate/settings.py) dodajmy nową listę STATICFILES_DIRS
```python

```

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
