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

@dataclass
class Vec2:
    x: int
    y: int

    def __add__(self, other):
        return Vec2(self[0]+other[0], self[1]+other[1])
    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        raise IndexError(f"Index: {item} does not exists in Vec2")

@dataclass
class Elf:
    cur_pos: Vec2
    proposed_pos: Optional[Vec2] = None
    is_alone: Optional[bool] = None

NORTH = Vec2(-1,0)
SOUTH = Vec2(1,0)
WEST = Vec2(0,-1)
EAST = Vec2(0,1)
FIRST_CHECK_LIST = [(a[0], b[1]) for a,b in itertools.product([(0,0), NORTH, SOUTH], [(0,0), WEST, EAST]) if not (a[0] == 0 and b[1] == 0)]

SECOND_MOVE_LIST = [(NORTH, [(-1,-1), (-1,0), (-1,1)]),
    (SOUTH, [(1,-1), (1,0), (1,1)]),
    (WEST, [(1,-1), (0,-1), (-1,-1)]),
    (EAST, [(1,1), (0,1), (-1,1)])
]


def parse_input(in_lines: List[str]):
    res = []
    for i,line in enumerate(in_lines):
        for j,ch in enumerate(line):
            if ch == "#":
                res.append(Elf(cur_pos=(i,j)))
    return res

def move(elfs: Dict[Tuple[int,int], Elf], round_num):
    for e in elfs.values():
        e.is_alone = all([(e.cur_pos[0]+dy, e.cur_pos[1]+dx) not in elfs for dy,dx in FIRST_CHECK_LIST])

    for e in elfs.values():
        if e.is_alone:
            continue
        e.proposed_pos = None
        for check_dir_ind in range(4):
            check_dir_ind = (check_dir_ind+round_num)%4
            direction, checks = SECOND_MOVE_LIST[check_dir_ind]
            if all([(e.cur_pos[0]+dy, e.cur_pos[1]+dx) not in elfs for dy,dx in checks]):
                e.proposed_pos = (e.cur_pos[0]+direction[0], e.cur_pos[1]+direction[1])
                break

    new_positions = {}
    for e in elfs.values():
        new_positions[e.proposed_pos] = new_positions.get(e.proposed_pos, 0)+1

    any_moved = False
    for e in elfs.values():
        if e.proposed_pos is not None and new_positions[e.proposed_pos] == 1:
            e.cur_pos = e.proposed_pos
            any_moved = True
        e.proposed_pos = None
        e.is_alone = None
    return any_moved

def show(elfs: List[Elf]):
    min_y = min([_.cur_pos[0] for _ in elfs])
    max_y = max([_.cur_pos[0] for _ in elfs])

    min_x = min([_.cur_pos[1] for _ in elfs])
    max_x = max([_.cur_pos[1] for _ in elfs])
    res = [["." for _ in range(min_x, max_x+1)] for _ in range(min_y, max_y+1)]
    for e in elfs:
        res[e.cur_pos[0]-min_y][e.cur_pos[1]-min_x] = "#"
    for row in res:
        print("".join(row))



def solve_first(parsed_input, num_iter=10):
    elfs: List[Elf] = parsed_input
    for i in range(num_iter):
        elfs_dict = {_.cur_pos:_ for _ in elfs}
        move(elfs_dict, i)

    # show(elfs)
    # print("----")

    min_y = min([_.cur_pos[0] for _ in elfs])
    max_y = max([_.cur_pos[0] for _ in elfs])

    min_x = min([_.cur_pos[1] for _ in elfs])
    max_x = max([_.cur_pos[1] for _ in elfs])
    # print(min_x, max_x, min_y, max_x)
    return (max_y-min_y+1)*(max_x-min_x+1)-len(elfs)


def solve_second(parsed_input, step=4):
    elfs: List[Elf] = parsed_input
    i = 0
    while True:
        elfs_dict = {_.cur_pos:_ for _ in elfs}
        if not move(elfs_dict, i):
            return i
        i += 1


if __name__ == '__main__':
    for solver in (
            solve_first,
            solve_second,
    ):

        with open("input1.txt") as file:
            lines = file.readlines()

        print("Example res", solver(parse_input(lines)))

        print("Test data")
        with open("input2.txt") as file:
            lines = file.readlines()
        print("Test res", solver(parse_input(lines)))
        print("-"*50)