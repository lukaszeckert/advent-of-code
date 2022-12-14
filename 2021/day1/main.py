import itertools
import operator
from typing import List

def solve(lines: List[str]):
    res = 0
    lines = list(map(int, map(str.strip, lines)))
    return sum([operator.lt(*_) for _ in zip(lines, lines[3:])])


if __name__ == '__main__':
    with open("input1.txt") as file:
        lines = file.readlines()
    print("Example res", solve(lines))

    print("Test data")
    with open("input2.txt") as file:
        lines = file.readlines()
    print("Test res", solve(lines))