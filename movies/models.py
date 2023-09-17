from django.db import models
import csv


# Create your models here.
class Movie:

    def __init__(self, tmdb_id, original_language, original_title, overview, popularity, release_date, title,
                 vote_average, vote_count):
        self.tmdb_id = int(tmdb_id)
        self.original_language = original_language
        self.original_title = original_title
        self.overview = overview
        self.popularity = popularity
        self.release_date = release_date
        self.title = title
        self.vote_average = float(vote_average)
        self.vote_count = int(vote_count)

    @staticmethod
    def get_all_movies():
        movies_arr = []
        with open('movies/migrations/movies_small.csv', 'r', encoding='utf-8') as all_movies_file:
            all_movies_file.readline()
            reader = csv.reader(all_movies_file, delimiter=',')

            for row in reader:
                movies_arr.append(Movie(*row))

        return movies_arr

    @staticmethod
    def find_by_tmdb_id(tmdb_id):
        with open('movies/migrations/movies_small.csv', 'r', encoding='utf-8') as all_movies_file:
            all_movies_file.readline()
            reader = csv.reader(all_movies_file, delimiter=',')

            for row in reader:
                movie = Movie(*row)
                if movie.tmdb_id == tmdb_id:
                    return movie

        return None
