import functools
import itertools
import multiprocessing
import operator
import re
import struct
from dataclasses import dataclass
from typing import List, Tuple, Dict
import tqdm


def parse_input(in_lines: List[str]):
      return [int(_.strip()) for _ in in_lines]


def solve_first(parsed_input, timelimit=24):
    data = [(_, i) for i,_ in enumerate(parsed_input)]
    moves = 0
    poz = 0
    while moves < len(data):
        if data[poz][1] == moves:
            moves += 1
            cur = data.pop(poz)
            n_poz = poz + cur[0]
            n_poz = (n_poz+len(data))%len(data)
            data.insert(n_poz, cur)
            # print(data)
        poz += 1
        poz %= len(data)

    data = [_[0] for _ in data]
    zero_index = data.index(0)
    res = 0
    for v in (1000,2000,3000):
        res += data[(v+zero_index)%len(data)]
        print(data[(v+zero_index)%len(data)])
    return res


def solve_second(parsed_input, timelimit=32):
    data = [(_*811589153, i) for i,_ in enumerate(parsed_input)]
    for _ in tqdm.tqdm(range(10)):
        moves = 0
        poz = 0
        while moves < len(data):
            if data[poz][1] == moves:
                moves += 1
                cur = data.pop(poz)
                n_poz = poz + cur[0]
                n_poz = (n_poz+len(data))%len(data)
                data.insert(n_poz, cur)
                # print(data)
            poz += 1
            poz %= len(data)

    data = [_[0] for _ in data]
    zero_index = data.index(0)
    res = 0
    for v in (1000,2000,3000):
        res += data[(v+zero_index)%len(data)]
        print(data[(v+zero_index)%len(data)])
    return res

if __name__ == '__main__':
    for solver in (
            # solve_first,
            solve_second,
    ):
        with open("input1.txt") as file:
            lines = file.readlines()

        print("Example res", solver(parse_input(lines)))

        print("Test data")
        with open("input2.txt") as file:
            lines = file.readlines()
        print("Test res", solver(parse_input(lines)))
