from imdb import IMDb
from typing import List, Dict, Tuple
import csv, requests, io
import pygame

ia = IMDb()


class Entry:
    """
    A base class for data entries
    """
    def __hash__(self) -> int:
        """
        Return the hash value of this data entry, based on the entry id
        Used to handle data entries being used as dictionary keys

        :return: the hashed value of this entry
        """
        return hash(self.id)


class Movie(Entry):
    """
    The data entry representing a movie
    """
    def __init__(self, movie: object, scores=(0, 0)) -> None:
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

    def basic_info(self) -> Dict:
        """
        Return basic info to display in tables

        :return: a dict with basic info
        """
        return {
            'id': self.id,
            'title': self.title,
            'info': f"{self.year if self.year is not None else '???'}"
        }


class Person(Entry):
    """
    The data entry representing a person
    """
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
        """
        Return basic info to display in tables

        :return: a dict with basic info
        """
        return {
            'id': self.id,
            'title': self.name,
            'info': self.birthdate
        }

    def get_ratings(self) -> Tuple[float, List[float]]:
        """
        Return the ratings of this person saved in the csv files

        :return: a tuple with a rating and a list of other ratings
        """
        savedata = load_person_ratings()
        if self.id in savedata:
            if savedata[self.id][0] == "null":
                return 5.5, [float(f) for f in savedata[self.id][1]]
            return float(savedata[self.id][0]), [float(f) for f in savedata[self.id][1]]
        else:
            return 5.5, []

    def __repr__(self):
        return self.name


def get_movie(id_: str) -> Movie:
    """
    Return a movie retrieved from IMDbPy by a given movie id

    :param id_: the IMDb id of a movie
    :return: a movie data entry
    """
    return Movie(ia.get_movie(id_, info=['main']))


def get_person(id_: str) -> Person:
    """
    Return a person retrieved from IMDbPy by a given person id

    :param id_: the IMDb id of a person
    :return: a person data entry
    """
    return Person(ia.get_person(id_, info=['main']))


def search_movie(query: str, amount: int) -> List[Movie]:
    """
    Return a number of search results based on a given query

    :param query: the movie title to search for
    :param amount: amount of results to return
    :return: list of movie search results
    """
    return [Movie(m) for m in list(ia.search_movie(query))[0:amount]]


def search_person(query: str, amount: int) -> List[object]:
    """
    Return a number of search results based on a given query

    :param query: the name of the person to search for
    :param amount: amount of results to return
    :return: list of people search results
    """
    return [Person(p) for p in list(ia.search_person(query))[0:amount]]


def update_movie(id_: str, tags: List[str]) -> Movie:
    """
    Return a movie with extra information

    :param id_: the id of the movie
    :param tags: the sets of data to retrieve from IMDbPy
    :return: a movie data entry
    """
    movie = ia.get_movie(id_)
    ia.update(movie, info=tags)
    return Movie(movie)


def update_person(id_: str, tags: List[str]) -> Person:
    """
    Return a person with extra information

    :param id_: the id of the person
    :param tags: the sets of data to retrieve from IMDbPy
    :return: a person data entry
    """
    person = ia.get_person(id_)
    ia.update(person, info=tags)
    return Person(person)


def save_person_rating(id_: str, rating: float, results: List[float]) -> None:
    """
    Save the ratings of a person to the csv files

    :param id_: the id of the person
    :param rating: the rating of the person
    :param results: the ratings of their movies
    """
    rows = load_person_ratings()
    rows[id_] = (rating, results)
    with open('people.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow([row, rows[row][0], *rows[row][1]])


def load_person_ratings() -> Dict:
    """
    Load the ratings of a person from the csv files

    :return: a dict of ratings for each person id
    """
    try:
        with open("people.csv", 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            return {k: (r, t) for k, r, *t in reader}
    except FileNotFoundError:
        _ = open("people.csv", 'x', newline='')
        return {}


def save_movie_rating(id_: str, prediction: float, rating: float) -> None:
    """
    Save the ratings of a movie to the csv files

    :param id_: the id of the movie
    :param prediction: the predicted score of the movie
    :param rating: the rating of the movie
    """
    rows = load_movie_ratings()
    rows[id_] = (prediction, rating)
    with open('movies.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow([row, rows[row][0], rows[row][1]])


def load_movie_ratings() -> Dict:
    """
    Load the ratings of a movie from the csv files

    :return: a dict of ratings for each movie id
    """
    try:
        with open("movies.csv", 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            return {k: (r, p) for k, r, p in reader}
    except FileNotFoundError:
        _ = open("movies.csv", 'x', newline='')
        return {}
