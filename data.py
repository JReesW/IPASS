from imdb import IMDb
from typing import List

ia = IMDb()


class Entry:
    def __hash__(self) -> int:
        return hash(self.id)


class Movie(Entry):
    def __init__(self, movie):
        self.id = movie.movieID
        self.title = movie.get('title')
        self.cast = movie.get('cast')
        self.scores = 0.0

    def basic_info(self):
        return {
            'id': self.id,
            'title': self.title,
            'info': "movie info here :)"
        }


class Person(Entry):
    def __init__(self, person):
        self.id = person.personID
        self.name = person['name']
        #self.biography = person['biography']
        self.scores = 0.0

    def basic_info(self):
        return {
            'id': self.id,
            'title': self.name,
            'info': "person info here ;D"
        }


def get_movie(id_: str) -> object:
    return Movie(ia.get_movie(id_))


def get_person(id_: str) -> object:
    return Person(ia.get_person(id_))


def search_movie(query: str, amount: int) -> List[object]:
    return [Movie(m) for m in list(ia.search_movie(query))[0:amount]]


def search_person(query: str, amount: int) -> List[object]:
    return [Person(p) for p in list(ia.search_person(query))[0:amount]]
