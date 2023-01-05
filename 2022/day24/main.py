import copy
import functools
import itertools
import multiprocessing
import operator
import re
import struct
from dataclasses import dataclass
from typing import List, Tuple, Dict, Union, Optional
import tqdm

@dataclass(frozen=True, eq=True)
class Vec2:
    x: int
    y: int

    def __add__(self, other):
        return Vec2(x=self.x+other.x, y=self.y+other.y)
    def __getitem__(self, item):
        if item == 0:
            return self.y
        elif item == 1:
            return self.x
        raise IndexError(f"Index: {item} does not exists in Vec2")

@dataclass
class Blizzard:
    pos: Vec2
    direction: Vec2

NORTH = Vec2(y=-1,x=0)
SOUTH = Vec2(y=1,x=0)
WEST = Vec2(y=0,x=-1)
EAST = Vec2(y=0,x=1)

def parse_input(in_lines: List[str]):
    return [_.strip()[::-1] for _ in in_lines]


def from_five(eq):
    cur = 0
    for i, ch in enumerate(eq):
        match ch:
            case "2":
                cur += 2 * (5 ** i)
            case "1":
                cur += 1 * (5 ** i)
            case "0":
                cur += 0 * (5 ** i)
            case "-":
                cur += -1 * (5 ** i)
            case "=":
                cur += -2 * (5 ** i)
            case _:
                print("aaa")
    return cur

def _tab_to_str(arr):
    res = ""
    if arr[-1] == 0:
        arr.pop()
    for ch in arr:
        match ch:
            case 1:
                res = res + "1"
            case 2:
                res = res + "2"
            case 0:
                res = res + "0"
            case -1:
                res = res + "-"
            case -2:
                res = res + "="
            case _:
                print("WFT", ch)
    return res

def to_five(num):
    res_five = []
    while num:
        cur = (num) % 5
        num //= 5
        res_five.append(cur)

    a = 0
    for i,v in enumerate(res_five):
        cur = v+a
        if cur == 3:
            res_five[i] = -2
            a = 1
        elif cur == 4:
            res_five[i] = -1
            a = 1
        elif cur == 5:
            res_five[i] = 0
            a = 1
        else:
            res_five[i] = cur
            a = 0
    if a > 0:
        res_five.append(a)

    res = ""

    for ch in res_five[::-1]:
        match ch:
            case 1:
                res = res + "1"
            case 2:
                res = res + "2"
            case 0:
                res = res + "0"
            case -1:
                res = res + "-"
            case -2:
                res = res + "="
            case _:
                print("WFT", ch)
    print(from_five(res[::-1]), res)
    return res


def solve_first(parsed_input, num_iter=10):
    res = 0
    for eq in parsed_input:
        cur = from_five(eq)
        res += cur

    print(res)
    res = to_five(res)
    return res

def solve_second(parsed_input, step=4):
    pass

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
        print("-"*50)