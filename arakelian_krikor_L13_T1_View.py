from tkinter import ttk
from tkinter import *
from arakelian_krikor_L13_T1_Model import *


# Populate functions
def populate_listbox_movies():
    try:
        movies.delete(0, END)
        for movie in model.movies.get_all():
            movies.insert(END, movie.title)
    except TypeError:
        pass


def populate_listbox_games():
    try:
        games.delete(0, END)
        for game in model.games.get_all():
            games.insert(END, game.title)
    except TypeError:
        pass


def populate_listbox_books():
    try:
        books.delete(0, END)
        for book in model.books.get_all():
            books.insert(END, book.title)
    except TypeError:
        pass


# Info functions
def movie_info(evt):
    if movies.curselection():
        title = movies.get(movies.curselection())
        m = model.movies.get_by_title(title)
        movies_L.config(text=f"Movie: {m.title}\n"
                             f"Genre: {m.genre}\n"
                             f"Released in: {m.release_year}\n"
                             f"Length: {m.length} minutes")


def game_info(evt):
    if games.curselection():
        title = games.get(games.curselection())
        g = model.games.get_by_title(title)
        games_L.config(text=f"Title: {g.title}\n"
                            f"Publisher: {g.publisher}\n"
                            f"Platform: {g.platform}\n" 
                            f"Genre: {g.genre}\n"
                            f"Released in: {g.release_year}")

def book_info(evt):
    if books.curselection():
        title = books.get(books.curselection())
        b = model.books.get_by_title(title)
        books_L.config(text=f"Title: {b.title}\n"
                            f"Author: {b.author}\n"
                            f"Publisher: {b.publisher}\n" 
                            f"ISBN: {b.isbn}\n"
                            f"Released in: {b.release_year}")


# Search functions
def search_movie_info(evt):
    if movies_search.curselection():
        title = movies_search.get(movies_search.curselection())
        m = model.movies.get_by_title(title)
        if m:
            movies_L.config(text=f"Movie: {m.title}\n"
                                 f"Genre: {m.genre}\n"
                                 f"Released in: {m.release_year}\n"
                                 f"Length: {m.length} minutes")


def search_game_info(evt):
    if games_search.curselection():
        title = games_search.get(games_search.curselection())
        g = model.games.get_by_title(title)
        if g:
            games_L.config(text=f"Title: {g.title}\n"
                                f"Publisher: {g.publisher}\n"
                                f"Platform: {g.platform}\n" 
                                f"Genre: {g.genre}\n"
                                f"Released in: {g.release_year}")


def search_book_info(evt):
    if books_search.curselection():
        title = books_search.get(books_search.curselection())
        b = model.books.get_by_title(title)
        if b:
            books_L.config(text=f"Title: {b.title}\n"
                                f"Author: {b.author}\n"
                                f"Publisher: {b.publisher}\n"
                                f"ISBN: {b.isbn}\n"
                                f"Released in: {b.release_year}")


# Delete functions
def del_movie():
    try:
        title = movies.get(movies.curselection())
    except:
        title = movies_search.get((movies_search.curselection()))
    movies.delete(movies.curselection())
    movies_L.config(text="")
    m = model.movies.get_by_title(title)
    model.movies.del_entry(m)
    populate_listbox_movies()
    model.write()


def del_game():
    try:
        title = games.get(games.curselection())
    except:
        title = games_search.get((games_search.curselection()))
    games.delete(games.curselection())
    games_L.config(text="")
    g = model.games.get_by_title(title)
    model.games.del_entry(g)
    populate_listbox_games()
    model.write()


def del_book():
    try:
        title = books.get(books.curselection())
    except:
        title = books_search.get((books_search.curselection()))
    books.delete(books.curselection())
    books_L.config(text="")
    b = model.books.get_by_title(title)
    model.books.del_entry(b)
    populate_listbox_books()
    model.write()


# Add functions
def new_movie_add(name, genre, release_year, length, window):
    model.movies.add_entry(Movie(name, genre, release_year, length))
    model.write()
    window.destroy()
    populate_listbox_movies()
    movies_L.config(text="")


def new_game_add(name, publisher, platform, genre, release_year, window):
    model.games.add_entry(Game(name, publisher, platform, genre, release_year))
    model.write()
    window.destroy()
    populate_listbox_games()
    games_L.config(text="")


def new_book_add(name, author, publisher, isbn, release_year, window):
    model.books.add_entry(Book(name,author, publisher, isbn, release_year))
    model.write()
    window.destroy()
    populate_listbox_books()
    books_L.config(text="")


# Edit functions
def edit_movie(selected_movie, name, genre, release_year, length, window):
    selected_movie.title = name
    selected_movie.genre = genre
    selected_movie.release_year = release_year
    selected_movie.length = length
    model.write()
    window.destroy()
    populate_listbox_movies()
    movies_L.config(text="")


def edit_game(selected_game, name, publisher, platform, genre, release_year, window):
    selected_game.title = name
    selected_game.publisher = publisher
    selected_game.platform = platform
    selected_game.genre = genre
    selected_game.release_year = release_year
    model.write()
    window.destroy()
    populate_listbox_games()
    games_L.config(text="")


def edit_book(selected_book, name, author, publisher, isbn, release_year, window):
    selected_book.title = name
    selected_book.author = author
    selected_book.publisher = publisher
    selected_book.isbn = isbn
    selected_book.release_year = release_year
    model.write()
    window.destroy()
    populate_listbox_books()
    books_L.config(text="")


# Pop up windows
def window_new_movie():
    add_movie_window = Toplevel(main_window)
    add_movie_window.title("Add movie")
    add_movie_window.geometry("300x200")
    add_movie_window.resizable(False, False)
    name = Entry(add_movie_window)
    name.grid(row=0, column=1)
    name_L = Label(add_movie_window, text="Title: ", justify=RIGHT)
    name_L.grid(row=0, column=0, sticky="e")
    genre = Entry(add_movie_window)
    genre.grid(row=1, column=1)
    genre_L = Label(add_movie_window, text="Genre: ", justify=RIGHT)
    genre_L.grid(row=1, column=0, sticky="e")
    release_year = Entry(add_movie_window)
    release_year.grid(row=2, column=1)
    release_year_L = Label(add_movie_window, text="Released in: ", justify=RIGHT)
    release_year_L.grid(row=2, column=0, sticky="e")
    length = Entry(add_movie_window)
    length.grid(row=3, column=1)
    length_L = Label(add_movie_window, text="Length in minutes: ", justify=RIGHT)
    length_L.grid(row=3, column=0, sticky="e")
    save = Button(add_movie_window, text="Save", command=lambda: new_movie_add(name.get(), genre.get(),
                                                                               release_year.get(), length.get(),
                                                                               add_movie_window))
    save.grid(row=4, column=0, columnspan=2)
    add_movie_window.focus()


def window_new_game():
    add_game_window = Toplevel(main_window)
    add_game_window.title("Add game")
    add_game_window.geometry("300x200")
    add_game_window.resizable(False, False)
    name = Entry(add_game_window)
    name.grid(row=0, column=1)
    name_L = Label(add_game_window, text="Title: ", justify=RIGHT)
    name_L.grid(row=0, column=0, sticky="e")
    publisher = Entry(add_game_window)
    publisher.grid(row=1, column=1)
    publisher_L = Label(add_game_window, text="Publisher: ", justify=RIGHT)
    publisher_L.grid(row=1, column=0, sticky="e")
    platform = Entry(add_game_window)
    platform.grid(row=2, column=1)
    platform_L = Label(add_game_window, text="Platform: ", justify=RIGHT)
    platform_L.grid(row=2, column=0, sticky="e")
    genre = Entry(add_game_window)
    genre.grid(row=3, column=1)
    genre_L = Label(add_game_window, text="Genre: ", justify=RIGHT)
    genre_L.grid(row=3, column=0, sticky="e")
    release_year = Entry(add_game_window)
    release_year.grid(row=4, column=1)
    release_year_L = Label(add_game_window, text="Released in: ", justify=RIGHT)
    release_year_L.grid(row=4, column=0, sticky="e")
    save = Button(add_game_window, text="Save", command=lambda: new_game_add(name.get(), publisher.get(),
                                                                             platform.get(), genre.get(),
                                                                             release_year.get(), add_game_window))
    save.grid(row=5, column=0, columnspan=2)
    add_game_window.focus()


def window_new_book():
    add_book_window = Toplevel(main_window)
    add_book_window.title("Add book")
    add_book_window.geometry("300x200")
    add_book_window.resizable(False, False)
    name = Entry(add_book_window)
    name.grid(row=0, column=1)
    name_L = Label(add_book_window, text="Title: ", justify=RIGHT)
    name_L.grid(row=0, column=0, sticky="e")
    author = Entry(add_book_window)
    author.grid(row=1, column=1)
    author_L = Label(add_book_window, text="Author: ", justify=RIGHT)
    author_L.grid(row=1, column=0, sticky="e")
    publisher = Entry(add_book_window)
    publisher.grid(row=2, column=1)
    publisher_L = Label(add_book_window, text="Publisher: ", justify=RIGHT)
    publisher_L.grid(row=2, column=0, sticky="e")
    isbn = Entry(add_book_window)
    isbn.grid(row=3, column=1)
    isbn_L = Label(add_book_window, text="ISBN: ", justify=RIGHT)
    isbn_L.grid(row=3, column=0, sticky="e")
    release_year = Entry(add_book_window)
    release_year.grid(row=4, column=1)
    release_year_L = Label(add_book_window, text="Released in: ", justify=RIGHT)
    release_year_L.grid(row=4, column=0, sticky="e")
    save = Button(add_book_window, text="Save", command=lambda: new_book_add(name.get(), author.get(), publisher.get(),
                                                                             isbn.get(), release_year.get(),
                                                                             add_book_window))
    save.grid(row=5, column=0, columnspan=2)


def window_edit_movie():
    try:
        title = movies.get(movies.curselection())
    except:
        title = movies_search.get((movies_search.curselection()))
    m = model.movies.get_by_title(title)
    edit_movie_window = Toplevel(main_window)
    edit_movie_window.title("Edit movie")
    edit_movie_window.geometry("300x200")
    edit_movie_window.resizable(False, False)
    name = Entry(edit_movie_window)
    name.insert(0, m.title)
    name.grid(row=0, column=1)
    name_L = Label(edit_movie_window, text="Title: ", justify=RIGHT)
    name_L.grid(row=0, column=0, sticky="e")
    genre = Entry(edit_movie_window)
    genre.insert(0, m.genre)
    genre.grid(row=1, column=1)
    genre_L = Label(edit_movie_window, text="Genre: ", justify=RIGHT)
    genre_L.grid(row=1, column=0, sticky="e")
    release_year = Entry(edit_movie_window)
    release_year.insert(0, m.release_year)
    release_year.grid(row=2, column=1)
    release_year_L = Label(edit_movie_window, text="Released in: ", justify=RIGHT)
    release_year_L.grid(row=2, column=0, sticky="e")
    length = Entry(edit_movie_window)
    length.insert(0, m.length)
    length.grid(row=3, column=1)
    length_L = Label(edit_movie_window, text="Length in minutes: ", justify=RIGHT)
    length_L.grid(row=3, column=0, sticky="e")
    save_m = Button(edit_movie_window, text="Save", command=lambda: edit_movie(m, name.get(), genre.get(),
                                                                             release_year.get(), length.get(),
                                                                             edit_movie_window))
    save_m.grid(row=4, column=0, columnspan=2)


def window_edit_game():
    try:
        title = games.get(games.curselection())
    except:
        title = games_search.get((games_search.curselection()))
    g = model.games.get_by_title(title)
    edit_game_window = Toplevel(main_window)
    edit_game_window.title("Edit game")
    edit_game_window.geometry("300x200")
    edit_game_window.resizable(False, False)
    name = Entry(edit_game_window)
    name.insert(0, g.title)
    name.grid(row=0, column=1)
    name_L = Label(edit_game_window, text="Title: ", justify=RIGHT)
    name_L.grid(row=0, column=0, sticky="e")
    publisher = Entry(edit_game_window)
    publisher.insert(0, g.publisher)
    publisher.grid(row=1, column=1)
    publisher_L = Label(edit_game_window, text="Publisher: ", justify=RIGHT)
    publisher_L.grid(row=1, column=0, sticky="e")
    platform = Entry(edit_game_window)
    platform.insert(0, g.platform)
    platform.grid(row=2, column=1)
    platform_L = Label(edit_game_window, text="Platform: ", justify=RIGHT)
    platform_L.grid(row=2, column=0, sticky="e")
    genre = Entry(edit_game_window)
    genre.insert(0, g.genre)
    genre.grid(row=3, column=1)
    genre_L = Label(edit_game_window, text="Genre: ", justify=RIGHT)
    genre_L.grid(row=3, column=0, sticky="e")
    release_year = Entry(edit_game_window)
    release_year.insert(0, g.release_year)
    release_year.grid(row=4, column=1)
    release_year_L = Label(edit_game_window, text="Released in: ", justify=RIGHT)
    release_year_L.grid(row=4, column=0, sticky="e")
    save_g = Button(edit_game_window, text="Save", command=lambda: edit_game(g, name.get(), publisher.get(),
                                                                           platform.get(), genre.get(),
                                                                           release_year.get(), edit_game_window))
    save_g.grid(row=5, column=0, columnspan=2)


def window_edit_book():
    try:
        title = books.get(books.curselection())
    except:
        title = books_search.get((books_search.curselection()))
    b = model.books.get_by_title(title)
    edit_book_window = Toplevel(main_window)
    edit_book_window.title("Edit book")
    edit_book_window.geometry("300x200")
    edit_book_window.resizable(False, False)
    name = Entry(edit_book_window)
    name.insert(0, b.title)
    name.grid(row=0, column=1)
    name_L = Label(edit_book_window, text="Title: ", justify=RIGHT)
    name_L.grid(row=0, column=0, sticky="e")
    author = Entry(edit_book_window)
    author.insert(0, b.author)
    author.grid(row=1, column=1)
    author_L = Label(edit_book_window, text="Author: ", justify=RIGHT)
    author_L.grid(row=1, column=0, sticky="e")
    publisher = Entry(edit_book_window)
    publisher.insert(0, b.publisher)
    publisher.grid(row=2, column=1)
    publisher_L = Label(edit_book_window, text="Publisher: ", justify=RIGHT)
    publisher_L.grid(row=2, column=0, sticky="e")
    isbn = Entry(edit_book_window)
    isbn.insert(0, b.isbn)
    isbn.grid(row=3, column=1)
    isbn_L = Label(edit_book_window, text="ISBN: ", justify=RIGHT)
    isbn_L.grid(row=3, column=0, sticky="e")
    release_year = Entry(edit_book_window)
    release_year.insert(0, b.release_year)
    release_year.grid(row=4, column=1)
    release_year_L = Label(edit_book_window, text="Released in: ", justify=RIGHT)
    release_year_L.grid(row=4, column=0, sticky="e")
    save_b = Button(edit_book_window, text="Save", command=lambda: edit_book(b, name.get(), author.get(), publisher.get(),
                                                                           isbn.get(), release_year.get(),
                                                                           edit_book_window))
    save_b.grid(row=5, column=0, columnspan=2)


# Search bars
def search_movie(title):
    movies_search.delete(0, END)
    try:
        m = model.movies.get_by_title(title)
        movies_search.insert(0, m.title)
    except:
        pass


def search_game(title):
    games_search.delete(0, END)
    try:
        g = model.games.get_by_title(title)
        games_search.insert(0, g.title)
    except:
        pass


def search_book(title):
    books_search.delete(0, END)
    try:
        b = model.books.get_by_title(title)
        books_search.insert(0, b.title)
    except:
        pass

model = GlobalData()

# Main program
main_window = Tk()
main_window.title("Collection Manager")
tabsController = ttk.Notebook(main_window)
tab_movies = Frame(tabsController)
tab_games = Frame(tabsController)
tab_books = Frame(tabsController)
tabsController.add(tab_movies, text="Movies")
tabsController.add(tab_games, text="Games")
tabsController.add(tab_books, text="Books")
tabsController.pack(expand=1, fill=BOTH)

# Buttons
# Movies
add_button = Button(tab_movies, text="Add Movie", command=window_new_movie)
add_button.grid(row=0, column=0)
edit_button = Button(tab_movies, text="Edit Movie", command=window_edit_movie)
edit_button.grid(row=0, column=1)
del_button = Button(tab_movies, text="Delete Movie", command=del_movie)
del_button.grid(row=0, column=2)
search_entry_m = Entry(tab_movies)
search_entry_m.grid(row=0, column=3)
search_button = Button(tab_movies, text="Search", command=lambda: search_movie(search_entry_m.get()))
search_button.grid(row=0, column=4)
#Games
add_button = Button(tab_games, text="Add Game", command=window_new_game)
add_button.grid(row=0, column=0)
edit_button = Button(tab_games, text="Edit Game", command=window_edit_game)
edit_button.grid(row=0, column=1)
del_button = Button(tab_games, text="Delete Game", command=del_game)
del_button.grid(row=0, column=2)
search_entry_g = Entry(tab_games)
search_entry_g.grid(row=0, column=3)
search_button = Button(tab_games, text="Search", command=lambda: search_game(search_entry_g.get()))
search_button.grid(row=0, column=4)
#Books
add_button = Button(tab_books, text="Add Book", command=window_new_book)
add_button.grid(row=0, column=0)
edit_button = Button(tab_books, text="Edit Book", command=window_edit_book)
edit_button.grid(row=0, column=1)
del_button = Button(tab_books, text="Delete Book", command=del_book)
del_button.grid(row=0, column=2)
search_entry_b = Entry(tab_books)
search_entry_b.grid(row=0, column=3)
search_button = Button(tab_books, text="Search", command=lambda: search_book(search_entry_b.get()))
search_button.grid(row=0, column=4)

# Listbox and labels
# Movies
movies = Listbox(tab_movies, selectmode=SINGLE, width=30, height=20, justify=LEFT)
movies.grid(column=0, row=1, sticky="nw")
movies_search = Listbox(tab_movies, selectmode=SINGLE, width=30, height=20, justify=LEFT)
movies_search.grid(column=3, columnspan=2, row=1, sticky="nw")
movies_L = Label(tab_movies, text="", justify=LEFT)
movies_L.grid(column=1, columnspan=2, row=1, sticky="nw")
movies.bind("<<ListboxSelect>>", movie_info)
movies_search.bind("<<ListboxSelect>>", search_movie_info)
# Games
games = Listbox(tab_games, selectmode=SINGLE, width=30, height=20, justify=LEFT)
games.grid(column=0, row=1, sticky="nw")
games_search = Listbox(tab_games, selectmode=SINGLE, width=30, height=20, justify=LEFT)
games_search.grid(column=3, columnspan=2, row=1, sticky="nw")
games_L = Label(tab_games, text="", justify=LEFT)
games_L.grid(column=1, columnspan=2, row=1, sticky="nw")
games.bind("<<ListboxSelect>>", game_info)
games_search.bind("<<ListboxSelect>>", search_game_info)
# Books
books = Listbox(tab_books, selectmode=SINGLE, width=30, height=20, justify=LEFT)
books.grid(column=0, row=1, sticky="nw")
books_search = Listbox(tab_books, selectmode=SINGLE, width=30, height=20, justify=LEFT)
books_search.grid(column=3, columnspan=2, row=1, sticky="nw")
books_L = Label(tab_books, text="", justify=LEFT)
books_L.grid(column=1, columnspan=2, row=1, sticky="nw")
books.bind("<<ListboxSelect>>", book_info)
books_search.bind("<<ListboxSelect>>", search_book_info)

model.load()
populate_listbox_movies()
populate_listbox_games()
populate_listbox_books()

main_window.mainloop()
