# Tworzenie nowej migracji

---
```text
Celem zadania jest utworzenie nowej aplikacji books, a w niej nowego modelu Book.
Tworzenie widoków oraz mapowania URL nie jest wymagane.
```
---
1) Proszę utworzyć nową aplikację o nazwie 'books'
2) Dodać nowo utworzoną aplikację w INSTALLED_APPS w pliku settings.py
3) Proszę dodać nowy model Book, który będzie Modelem Django. Zmienne klasy:
   - Nazwa Książki, maksymalna długość - 255
   - Data wydania Książki
   - Średnia ocena Książki
   - Liczba głosów
4) Proszę wykonać migrację modelu do bazy danych (bez danych początkowych)

---

## Demo save() i all()

---

1) Dodanie nowego pola autor z domyślną wartością null
2) Dodanie walidatorów na polu średnia ocena, wartość z zakresu 1-10
3) Wykonanie migracji