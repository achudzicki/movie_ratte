# Gotowe Rozwiązanie Django.

- Sprawdzenie co mamy pod url http://127.0.0.1:8000/admin
- Utworzenie nowego super użytkownika
```python
python manage.py createsuperuser
```
- dodanie naszych modeli do panelu admina w plikach 
  - [admin.py dla movies](movies/admin.py)
  - [admin.py dla books](books/admin.py)