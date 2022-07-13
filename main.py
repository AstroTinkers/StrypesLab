from tkinter import *
from tkinter import ttk

class Movies:

    movie_dict = {}

    def add_movie(self, title, year, director, length, genre, budget, rating):
        Movies.movie_dict[(title, year)] = {
                             'director': director,
                             'length': length,
                             'genre': [genr for genr in genre],
                             'budget': budget,
                             'rating': rating}

    def delete_movie(self, movie, year):
        Movies.movie_dict.pop((movie, year))

    def view_movie_details(self, movie, year):
        return Movies.movie_dict[(movie, year)]

    def view_movie_director(self, movie, year):
        return Movies.movie_dict[(movie, year)]['director']

    def view_highest_rating(self):
        highest_rating = 0
        highest_movie = ''
        for movie in Movies.movie_dict:
            if Movies.movie_dict[movie]['rating'] > highest_rating:
                highest_rating = Movies.movie_dict[movie]['rating']
                highest_movie = movie[0]

        return f"Movie with the highest rating -> {highest_movie}, {highest_rating}"


movie_collection = Movies()
movie_collection.add_movie('Spider-Man: No way home', 2021, 'Jon Watts', 148, ['Action', 'Fantasy'], 5500000, 8.3)
movie_collection.add_movie('Top Gun: Maverick', 2022, 'Joseph Kosinski', 130, ['Action', 'Drama'], 3200000, 8.6)
movie_collection.add_movie('The Batman', 2022, 'Matt Reeves', 176, ['Action', 'Crime'], 1520000, 7.9)

print(movie_collection.view_highest_rating())
print(movie_collection.view_movie_director('The Batman', 2022))

with open('movies.txt', 'w') as movies:
    movies.write(str(Movies.movie_dict))

# Visual
def delete_pair():
    searched_pair = text_entry.get().split()
    name = ' '.join(searched_pair[:-1])
    year = int(searched_pair[-1])
    data = movie_collection.movie_dict[(name, year)]
    movie_collection.delete_movie(name, year)

def get_pair():
    try:
        searched_pair = text_entry.get().split()
        name = ' '.join(searched_pair[:-1])
        year = int(searched_pair[-1])
        data = movie_collection.movie_dict[(name, year)]
        director_info.config(text=f"Director: {data['director']}")
        length_info.config(text=f"Length: {data['length']} min")
        genre_info.config(text=f"Genre: {', '.join(data['genre'])}")
        budget_info.config(text=f"Budget: {data['budget']}$")
        rating_info.config(text=f"Rating: {data['rating']} *")
        error.config(text='')
    except (IndexError, KeyError) as e:
        error.config(text='Movie is not available')

root = Tk()
root.title("Movies")
root.geometry('400x400')

mainframe = ttk.Frame(root)
mainframe.grid(row=0, column=0, sticky='nsew')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

error = Label(mainframe, text='', fg='red')
error.grid(row=1, columnspan=3, column=0, sticky='we')
text = Label(mainframe, text='Please write the title and the year of the movie you are looking for:')
text.grid(row=2, columnspan=3, column=0, sticky='we')

text_entry = ttk.Entry(mainframe)
text_entry.grid(row=3, column=0, columnspan=4, sticky='we')

search_button = ttk.Button(mainframe, text='SEARCH...', command=get_pair)
search_button.grid(row=4, column=0, sticky='we')

delete_button = ttk.Button(mainframe, text='DELETE FILM', command=delete_pair)
delete_button.grid(row=4, column=1, sticky='we')

director_info = Label(mainframe, text='Director: ')
director_info.grid(row=5, column=0, sticky='we')

length_info = Label(mainframe, text='Length: ')
length_info.grid(row=6, column=0, sticky='we')

genre_info = Label(mainframe, text='Genre: ')
genre_info.grid(row=7, column=0, sticky='we')

budget_info = Label(mainframe, text='Budget: ')
budget_info.grid(row=8, column=0, sticky='we')

rating_info = Label(mainframe, text='Rating:')
rating_info.grid(row=9, column=0, sticky='we')

root.mainloop()