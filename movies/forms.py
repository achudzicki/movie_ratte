from django import forms


# Ważne! Dziedziczymy po klasie forms z Django.
# Bardzo podobne definiowanie dla modelu encji bazodanowej.
class MovieForm(forms.Form):
    tmdb_id = forms.CharField(max_length=50, required=False, label='TMDB ID')
    title = forms.CharField(max_length=255, required=True, label='Tytuł')
    overview = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    release_date = forms.DateField(label='Data wydania')
    cast = forms.CharField(max_length=255, label='Obsada')
    genres = forms.CharField(max_length=255, label="Gatunki (rozdzielone '|')")
    director = forms.CharField(max_length=255, label='Reżyser')
    keywords = forms.CharField(max_length=1000, label='Słowa kluczowe')
