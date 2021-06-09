from typing import Tuple, List


class WeightedPattern:
    def __init__(self, length: int) -> None:
        self.length = length
        self.matrix = {}

    # Adds a new row for a given data entry
    def add_row(self, data: object) -> None:
        self.matrix[data] = generate_row(data.scores, self.length)

    # Get a specific weight via square bracket indexing, according to definition 1 of the paper
    def __getitem__(self, item: Tuple[int, object]) -> float:
        return self.matrix[item[1]][item[0] - 1]

    # Returns the score of a given pattern, according to definition 2 of the paper
    def score(self, pattern: List[object]) -> float:
        result = 0
        for c, p in enumerate(pattern):
            if c >= self.length:
                break
            result += self[c + 1, p]
        return result


class DataEntry:
    def __init__(self, id_: int, name: str, scores) -> None:
        self.id = id_
        self.name = name
        self.scores = scores

    # Makes this object hashable, so it can be used as a dictionary key
    def __hash__(self) -> int:
        return hash(self.id)


# TEMPORARY
def generate_row(scores: float, length: int) -> List[float]:
    return [scores - e for e in range(length)]


# TEST VALUES
data1 = DataEntry(1234, "Jeff", 8)
data2 = DataEntry(1235, "Mike", 4)
test = WeightedPattern(6)
test.add_row(data1)
test.add_row(data2)
print(test[2, data1])
print(test.score([data2, data1]))
