import itertools
import operator
import struct
from typing import List

def solve(lines: List[str]):
    cur = lines[0].strip()

    lines = lines[2:]

    lines = {_[0].strip():_[1].strip() for _ in [line.split(" -> ")for line in lines]}


    for _ in range(10):
        next_line = ""
        for ch, next_ch in zip(cur, cur[1:]):
            next_line += ch
            next_line += lines.get(ch+next_ch, "")
        next_line += next_ch
        cur = next_line

    res = sorted([len(list(_[1])) for _ in itertools.groupby(sorted(cur))])

    return res[-1]-res[0]


if __name__ == '__main__':
    with open("input1.txt") as file:
        lines = file.readlines()
    print("Example res", solve(lines))

    print("Test data")
    with open("input2.txt") as file:
        lines = file.readlines()
    print("Test res", solve(lines))