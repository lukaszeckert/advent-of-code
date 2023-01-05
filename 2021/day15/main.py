import itertools
import operator
import struct
from dataclasses import dataclass
from typing import List

def parse_input(in_lines: List[str]):
    in_lines = [_.strip() for _ in in_lines]

    return in_lines

def solve_first(parsed_input):
    res = 0
    return res

def solve_second(parsed_input):
    
    return res



if __name__ == '__main__':
    for solver in (
        solve_first,
        # solve_second,
    ):
        with open("input1.txt") as file:
            lines = file.readlines()

        print("Example res", solver(parse_input(lines)))

        print("Test data")
        with open("input2.txt") as file:
            lines = file.readlines()
        print("Test res", solver(parse_input(lines)))


