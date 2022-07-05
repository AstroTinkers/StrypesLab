import tkinter
from tkinter import *


class Movie:
    def __init__(self):
        self.movie_name = str()
        self.movie_genre = str()
        self.release_year = int()
        self.movies = dict()

    def add_movie(self, movie_name, movie_genre=None, release_year=None):
        self.movie_name = movie_name
        self.movie_genre = movie_genre
        self.release_year = release_year
        self.movies[movie_name] = {'Genre': movie_genre, 'Release Year': release_year}

    def add_genre(self, movie, genre):
        self.movies[movie]['Genre'] = genre

    def add_year(self, movie, year):
        self.movies[movie]['Release Year'] = year

    def search_movie(self, search_word):
        if search_word in self.movies:
            return f'Movie: {search_word} Genre: {self.movies[search_word]["Genre"]} Release year:' \
                   f' {self.movies[search_word]["Release Year"]}'
        else:
            return 'Not found'


movies = Movie()
movies.add_movie('Terminator', 'Action', 1989)
movies.add_movie('Terminator 2', 'Action', 1991)
movies.add_movie('Avatar')
movies.add_movie('Star Wars')
movies.add_movie('Jurassic Park', release_year=1990)
print(movies.search_movie('Terminator'))
print(movies.movies['Star Wars'])
movies.add_genre('Star Wars', 'Space Opera')
print(movies.search_movie('Star Wars'))
movies.add_year('Star Wars', 1977)
print(movies.search_movie('Star Wars'))
