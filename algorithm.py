from typing import Tuple, List, Union
from copy import copy
import data
import math


"""
CITATIONS:

[1] Salmela L., Tarhio J. (2007) Algorithms for Weighted Matching.
    In: Ziviani N., Baeza-Yates R. (eds) String Processing and Information Retrieval.
    SPIRE 2007. Lecture Notes in Computer Science, vol 4726.
    Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-540-75530-2_25

"""


class WeightedPattern:
    def __init__(self, length: int) -> None:
        """
        Initialize a weighted pattern with a given length

        :param length: the ammount of position indices in the weighted pattern
        """
        self.length = length
        self.matrix = {}

    # Add a new row for a given data entry
    def add_row(self, info: object) -> None:
        """
        Add a filled row for a given data entry.

        :param info: an Entry instance, see data.py
        """
        self.matrix[info] = generate_row(info.get_ratings(), self.length)

    # Get a specific weight via square bracket indexing, according to definition 1 of the paper
    # Or get a segment of the entire matrix using slice indexing, as used in definition 4 of the paper
    def __getitem__(self, item: Union[Tuple[int, object], slice]) -> Union[object, float]:
        """
        Return a weight from the weighted pattern, given a position and a data entry.
        Optional: returns a sliced weighted pattern when given a slice object.
        Used to handle square-bracket indexing on the weighted pattern.

        :param item: the index/slice to specify what part to return
        :return: a weight or a sliced weighted pattern
        """
        if isinstance(item, slice):
            return self.slice(item)
        return self.matrix[item[1]][item[0] - 1]

    # Return the length of the weighted pattern (positions, not objects)
    def __len__(self) -> int:
        """
        Return the amount of position indices in this weighted pattern.
        Used too handle len() on the weighted pattern

        :return: the length
        """
        return self.length

    # Return the score of a given pattern, according to definition 2 of the paper
    def score(self, pattern: List[object]) -> float:
        """
        Return the score of a weighted pattern given a pattern of data entries,
        as described in Definition 2 of citation 1

        :param pattern: a list of data entries
        :return: the score of the pattern
        """
        result = 0
        for c, p in enumerate(pattern):
            if c >= self.length:
                break
            result += self[c + 1, p]
        return result

    # Return a segment of the weighted pattern as a new weighted pattern, using vertical slices
    def slice(self, segment: slice) -> object:
        """
        Return a horizontal slice of the weighted pattern given a slice object.
        The slice indicates the positional indices to use.

        :param segment: a slice object with a start and a stop
        :return: a new weighted pattern
        """
        start, stop = segment.start, segment.stop
        result = WeightedPattern(stop - (start - 1))
        result.matrix = {obj: scores[start - 1:stop] for obj, scores in self.matrix.items()}
        return copy(result)

    # Return the p-value of the weighted pattern, according to definition 4
    def pvalue(self, threshold: float) -> float:
        """
        Return the p-value of a weighted pattern, which is the chance that the score passes the given threshold,
        as described in Definition 4 of citation 1

        :param threshold: the threshold to surpass
        :return: the chance that the score surpasses the threshold [0...1]
        """
        # Recursion end-case
        if len(self) == 0:
            return 1 if threshold <= 0 else 0

        sigma = self.matrix.keys()
        delta = len(sigma)
        i = len(self)
        return sum([self[1:i-1].pvalue(threshold - self[i, c]) for c in sigma]) / delta


def generate_row(scores: Tuple[float, List[float]], length: int) -> List[float]:
    """
    Return a new row for the weighted pattern filled with weights for a given set of ratings.

    :param scores: the rating of the actor and a list of ratings their movies got
    :param length: declares how many values the row will contain.
    :return: a new row containing weights
    """
    result = []
    rating, previous = scores
    for pos in range(1, length + 1):
        diff = rating - 5.5
        compared = diff + compare_ratings(rating, previous)
        result.append(rating + (compared * impact(pos)))
    return result


# Gives an impact score for a given position
def impact(pos: float) -> float:
    """
    Return an impact factor, depending on the given positional index of an actor.

    :param pos: the positional index of an actor
    :return: the impact factor of their position
    """
    if pos < 9:
        return math.sin((pos + 3) * (math.pi / 8)) + 1
    return 0


def compare_ratings(rating: float, previous: List[float]) -> float:
    """
    Return the average of how much the final film scores differ from the rating given to the actor

    :param rating: the rating given to the actor
    :param previous: list of ratings of movies this actor has been in
    :return: the average of the differences
    """
    return (sum([f - rating for f in previous]) / max(1, len(previous))) / 10
