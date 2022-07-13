import json
class Entity:
    def __init__(self, title):
        if not title:
            raise ValueError("Title should be populated")
        self.title = title

class Game(Entity):
    def __init__(self, title, publisher=None, platform=None, genre=None, release_year=None):
        super().__init__(title)
        self.publisher = publisher
        self.platform = platform
        self.genre = genre
        self.release_year = release_year

    def __repr__(self):
        publisher = self.publisher or "N/A"
        platform = self.platform or "N/A"
        genre = self.genre or "N/A"
        release_year = self.release_year or "N/A"
        return f"Game Title: {self.title}, Published by: {publisher}, Available on: {platform}, Genre: {genre}, " \
               f"Released: {release_year}."

    # def __eq__(self, other):
    #     return self.title == other.title and self.genre = other.genre...

class Movie(Entity):
    pass
class Book(Entity):
    pass

class EntityService:
    def __init__(self):
        self._store = []
    def add(self, entity: Entity):
        # EntityService can check if it operates on Entity()s and not strings/dicts/etc
        # if entity is not Entity:
        #     raise ValueError()

        # possible duplication check
        # # relies on __eq__ on entity()
        # if entity in self._store:
        #     return False
        self._store.append(entity)
        # return True
    def delete(self, entity: Entity):
        self._store.remove(entity)
    def get_all(self):
        return self._store
    def find_duplicates(self, predicate):
        return [predicate(e) for e in self._store] # relies on __eq__ in Entity

class MovieService(EntityService):
    pass
    # add in child can check for duplicates? then EntityService.add should not check for duplicates
    # def add(self, movie: Movie):
    #     if movie is not Movie:
    #         return False
    #     EntityService.add(self, movie)
    #     return True

class BookService(EntityService):
    pass
class GameService(EntityService):
    # additional functionality specific to games only
    def search(self, name):
        for m in self._store:
            if m.name == name:
                return name
        return None
    pass

# holds movies, games, books as fields
class GlobalData:
    def __init__(self):
        self.movies = MovieService()
        self.games = GameService()
        self.books = BookService()

    def write(self):
        root = {
            "movies": [m.__dict__ for m in self.movies.get_all()],
            "games": [g.__dict__ for g in self.games.get_all()],
            "books": [b.__dict__ for b in self.books.get_all()],
        }
        print(json.dumps(root))

# needs to inject services as they're not accessible otherwise as fields, as they're not stored
class JsonDatabaseManager:
    def write(self, movie_service: MovieService, book_service: BookService, game_service: GameService):
        root = {
            "movies": [m.__dict__ for m in movie_service.get_all()],
            "games": [g.__dict__ for g in game_service.get_all()],
            "books": [b.__dict__ for b in book_service.get_all()],
        }
        print(json.dumps(root))

    def load(self):
        content = json.loads('{"movies": [], "games": [{"title": "God of Lore 3", "publisher": "Eidos", "platform": "PS3", "genre": "action", "release_year": 2010}], "books": []}')
        movies = []
        games = [Game(g["title"], g["publisher"], g["platform"], g["genre"], g["release_year"]) for g in content["games"]]
        books = []
        return { # return same structure as self.write()
            "movies": movies,
            "games": games,
            "books": books,
        }

# another write/load implementation
class BinaryDatabaseManager:
    def write(self, movie_service: MovieService, book_service: BookService, game_service: GameService):
        # use pickle
        g = Game(None).genre
        print(f"{g}")
        pass

# ---------------------------------------

# UI code
# from model import *

movies = MovieService()
books = BookService()
games = GameService()

# # implementation with search method on service
# search_string = "God of l"
# if games.search(lambda g: g.title == search_string):
#     # tell user "BAD"
#     pass
#
# # implementation with service.add() returning True/False on duplication
# if games.add(Game(search_string)):
#     # tell user "OK"
#     pass
# else:
#     # tell user "BAD"
#     pass
#

games.add(Game("God of Lore 3", "Eidos", "PS3", "action", 2010))
JsonDatabaseManager().write(movies, books, games)
load_result = JsonDatabaseManager().load()
for g in load_result["games"]:
    games.add(g)

print(games.get_all())


# gd = GlobalData()
#
# #page1
# gd.movies.add(Movie())
# gd.write()
#
#
# #page2
# gd.games.add(Game(None))