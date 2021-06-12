from typing import Tuple, List, Union
from copy import copy
import data


class WeightedPattern:
    def __init__(self, length: int) -> None:
        self.length = length
        self.matrix = {}

    # Add a new row for a given data entry
    def add_row(self, info: object) -> None:
        self.matrix[info] = generate_row(info.scores, self.length)

    # Get a specific weight via square bracket indexing, according to definition 1 of the paper
    # Or get a segment of the entire matrix using slice indexing, as used in definition 4 of the paper
    def __getitem__(self, item: Union[Tuple[int, object], slice]) -> Union[object, float]:
        if isinstance(item, slice):
            return self.slice(item)
        return self.matrix[item[1]][item[0] - 1]

    # Return the length of the weighted pattern (positions, not objects)
    def __len__(self):
        return self.length

    # Return the score of a given pattern, according to definition 2 of the paper
    def score(self, pattern: List[object]) -> float:
        result = 0
        for c, p in enumerate(pattern):
            if c >= self.length:
                break
            result += self[c + 1, p]
        return result

    # Return a segment of the weighted pattern as a new weighted pattern, using vertical slices
    def slice(self, segment):
        start, stop = segment.start, segment.stop
        result = WeightedPattern(stop - (start - 1))
        result.matrix = {obj: scores[start - 1:stop] for obj, scores in self.matrix.items()}
        return copy(result)

    # Return the p-value of the weighted pattern, according to definition 4
    def pvalue(self, threshold: float):
        # Recursion end-case
        if len(self) == 0:
            return 1 if threshold <= 0 else 0

        sigma = self.matrix.keys()
        delta = len(sigma)
        i = len(self)
        return sum([self[1:i-1].pvalue(threshold - self[i, c]) for c in sigma]) / delta


# TEMPORARY
def generate_row(scores: float, length: int) -> List[float]:
    return [scores - e for e in range(length)]


# TEST VALUES
# data1 = DataEntry(1234, "Jeff", 8)
# data2 = DataEntry(1235, "Mike", 4)
# data3 = DataEntry(1236, "Tim", 9)
# data4 = DataEntry(1237, "Tom", 2)
# data5 = DataEntry(1238, "Rich", 4)
# data6 = DataEntry(1239, "Jake", 2)
#
# test = WeightedPattern(6)
#
# test.add_row(data1)
# test.add_row(data2)
# test.add_row(data3)
# test.add_row(data4)
# test.add_row(data5)
# test.add_row(data6)
#
# test2 = test[1:3]
# print(test.matrix[data4])
# print(test2.matrix[data4])
# print(len(test))
# print(len(test2))
#
# print(test.pvalue(20))
