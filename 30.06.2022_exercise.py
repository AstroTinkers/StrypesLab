import json


class Entity:
    def __init__(self, title):
        if not title:
            raise ValueError("Title should be populated.")
        self.title = title


class Movie(Entity):
    def __init__(self, title, genre=None, release_year=None, length=None):
        super().__init__(title)
        self.genre = genre
        self.release_year = release_year
        self.length = length


class Game(Entity):
    def __init__(self, title, publisher=None, platform=None, genre=None, release_year=None):
        super().__init__(title)
        self.publisher = publisher
        self.platform = platform
        self.genre = genre
        self.release_year = release_year


class Book(Entity):
    def __init__(self, title, author=None, publisher=None, isbn=None, release_year=None):
        super().__init__(title)
        self.author = author
        self.publisher = publisher
        self.isbn = isbn
        self.release_year = release_year


class EntityService:
    def __init__(self):
        self._store = []

    def add_entry(self, entity: Entity):
        # if entity is not Entity:  # Check if input data is valid.
        #     raise ValueError
        if entity in self._store:  # Check for duplicate input.
            return False
        self._store.append(entity)
        return True

    def del_entry(self, entity: Entity):
        self._store.remove(entity)

    def get_all(self):
        return self._store


class MovieService(EntityService):
    def search(self, title):
        for name in self._store:
            if name.title == title:
                return title
        return None


class GameService(EntityService):
    def search(self, title):
        for name in self._store:
            if name.title == title:
                return title
        return None


class BookService(EntityService):
    def search(self, title):
        for name in self._store:
            if name.title == title:
                return title
        return None


class GlobalData:
    """Holds movies, games and books as fields"""
    def __init__(self):
        self.movies = MovieService()
        self.games = GameService()
        self.books = BookService()

    def write(self):
        root = {
            "Movies": [m.__dict__ for m in self.movies.get_all()],
            "Games": [g.__dict__ for g in self.games.get_all()],
            "Books": [b.__dict__ for b in self.books.get_all()]
        }
        with open("database.txt", "w") as database:
            json.dump(root, database, indent=4)
        database.close()

    def load(self):
        try:
            with open("database.txt", "r") as database:
                content = json.load(database)
            self.movies = [Movie(m["title"], m["genre"], m["release_year"], m["length"]) for m in content["Movies"]]
            self.games = [Game(g["title"], g["publisher"], g["platform"], g["genre"], g["release_year"]) for g in content["Games"]]
            self.books = [Book(b["title"], b["author"], b["publisher"], b["isbn"], b["release_year"]) for b in content["Books"]]
            database.close()
        except json.decoder.JSONDecodeError:
            self.movies = None
            self.games = None
            self.books = None
        return {
            "Movies": self.movies,
            "Games": self.games,
            "Books": self.books
        }
