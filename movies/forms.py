import datetime

from django import forms
from django.core.exceptions import ValidationError


def validate_date(date: datetime.date):
    now = datetime.date.today()
    if date >= now:
        raise ValidationError('Data powinna być w przeszłości!', code='date_in_future')


# Ważne! Dziedziczymy po klasie forms z Django.
# Bardzo podobne definiowanie dla modelu encji bazodanowej.

# Max Length i required będą widoczne w Tagach HTML.
class MovieForm(forms.Form):
    tmdb_id = forms.CharField(max_length=50, required=False, label='TMDB ID')
    title = forms.CharField(max_length=255, label='Tytuł')
    overview = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    release_date = forms.DateField(label='Data produkcji', widget=forms.DateInput(attrs={"type": "date"}),
                                   validators=[validate_date])
    cast = forms.CharField(max_length=255, label='Obsada')
    genres = forms.CharField(max_length=255, label="Gatunki (rozdzielone '|')")
    director = forms.CharField(max_length=255, label='Reżyser')
    keywords = forms.CharField(max_length=1000, label='Słowa kluczowe')

    # Teraz trik, żeby dodać do każdego z naszych input klasę 'uk-input'
    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = f'Pole {field.label} jest wymagane'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'uk-input'


# Drugi sposób na zdefiniowanie naszego formularza
# W tym wypadku nasz formularz zostanie automatycznie wygenerowany z naszego modelu
from .models import Movie


class MovieFormTwo(forms.ModelForm):
    # Musimy podać nasz model z którego ma zostać wygenerowany formularz

    def __init__(self, *args, **kwargs):
        super(MovieFormTwo, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages['required'] = f'Pole {field.label} jest wymagane'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'uk-input'

    class Meta:
        model = Movie
        # Pole fields - można podać jakie pola mają zostać wygenerowane.
        # fields = "__all__"
        # fields = ["tmdb_id", "overview"]
        # Nam łatwiej jest podać jakie pola, nie zostaną wygenerowane. ID nigdy nie zostanie dodane do formularza.
        exclude = ['statistics']

        # Teraz możemy zdefiniować nasze labele, jako klucz-wartość (nazwa pola)
        labels = {
            'tmdb_id': 'TMDB ID',
            'original_title': 'Tytuł',
            'overview': 'Opis',
            'release_date': 'Data produkcji',
            'cast': 'Obsada',
            'genres': 'Gatunki',
            'director': 'Reżyser',
            'keywords': 'Słowa kluczowe',
        }
        widgets = {
            'release_date': forms.DateInput(attrs={"type": "date"})
        }

        # Validatory trzeba przenieść na Model
