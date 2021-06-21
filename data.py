from imdb import IMDb
from typing import List
import csv, requests, io
import pygame

ia = IMDb()


class Entry:
    def __hash__(self) -> int:
        return hash(self.id)


class Movie(Entry):
    def __init__(self, movie, scores=(0,0)):
        self.id = movie.movieID
        self.title = movie.get('title')
        cast = movie.get('cast')
        self.cast = [Person(p) for p in cast] if cast is not None else []
        directors = movie.get('directors')
        self.directors = [Person(p) for p in directors] if directors is not None else []
        self.year = movie.get('year')
        try:
            url = movie.get('cover url')
            if url is not None and "_CR" in url:
                url = url[:-22]
                self.url = url + "450_CR0,0,303,450_.jpg" if url[-1] == "Y" else url + "303_CR0,0,303,450_.jpg"
            else:
                self.url = url
            r = requests.get(self.url)
            self.poster = pygame.image.load_extended(io.BytesIO(r.content), self.url)
        except requests.exceptions.RequestException:
            self.poster = None
        self.scores = scores

    def basic_info(self):
        return {
            'id': self.id,
            'title': self.title,
            'info': f"{self.year if self.year is not None else '???'}"
        }


class Person(Entry):
    def __init__(self, person, scores=(0,[0])):
        self.id = person.personID
        self.name = person.get('name')
        self.birthdate = person.get('birth date')
        birthinfo = person.get('birth info')
        self.birthplace = birthinfo['birth place'] if birthinfo is not None else ""
        try:
            url = person.get('headshot')
            if "_CR" in url:
                url = url[:-22]
                self.url = url + "450_CR0,0,303,450_.jpg" if url[-1] == "Y" else url + "303_CR0,0,303,450_.jpg"
            else:
                self.url = url
            r = requests.get(self.url)
            self.headshot = pygame.image.load_extended(io.BytesIO(r.content), self.url)
        except Exception:
            self.headshot = None
        self.scores = scores

    def basic_info(self):
        return {
            'id': self.id,
            'title': self.name,
            'info': self.birthdate
        }

    def __repr__(self):
        return self.name


def get_movie(id_: str) -> object:
    return Movie(ia.get_movie(id_, info=['main']))


def get_person(id_: str) -> object:
    return Person(ia.get_person(id_, info=['main']))


def search_movie(query: str, amount: int) -> List[object]:
    return [Movie(m) for m in list(ia.search_movie(query))[0:amount]]


def search_person(query: str, amount: int) -> List[object]:
    return [Person(p) for p in list(ia.search_person(query))[0:amount]]


def update_movie(id_: str, tags: List[str]) -> object:
    movie = ia.get_movie(id_)
    ia.update(movie, info=tags)
    return Movie(movie)


def update_person(id_: str, tags: List[str]) -> object:
    person = ia.get_person(id_)
    ia.update(person, info=tags)
    return Person(person)


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
