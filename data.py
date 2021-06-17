from imdb import IMDb
from typing import List
import csv

ia = IMDb()


class Entry:
    def __hash__(self) -> int:
        return hash(self.id)


class Movie(Entry):
    def __init__(self, movie, scores=(0,0)):
        self.id = movie.movieID
        self.title = movie.get('title')
        self.cast = movie.get('cast')
        self.scores = scores

    def basic_info(self):
        return {
            'id': self.id,
            'title': self.title,
            'info': "movie info here :)"
        }


class Person(Entry):
    def __init__(self, person, scores=(0,[0])):
        self.id = person.personID
        self.name = person['name']
        #self.biography = person['biography']
        self.scores = scores

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


def save_person_rating(id_, rating, results):
    rows = load_person_ratings()
    rows[id_] = (rating, results)
    with open('people.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow([row, rows[row][0], *rows[row][1]])


def load_person_ratings():
    try:
        with open("people.csv", 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            return {k: (r, t) for k, r, *t in reader}
    except FileNotFoundError:
        _ = open("people.csv", 'x', newline='')
        return {}


def save_movie_rating(id_, rating, prediction):
    rows = load_movie_ratings()
    rows[id_] = (rating, prediction)
    with open('movies.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow([row, rows[row][0], rows[row][1]])


def load_movie_ratings():
    try:
        with open("movies.csv", 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            return {k: (r, p) for k, r, p in reader}
    except FileNotFoundError:
        _ = open("movies.csv", 'x', newline='')
        return {}
