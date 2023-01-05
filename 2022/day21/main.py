import copy
import functools
import itertools
import multiprocessing
import operator
import re
import struct
from dataclasses import dataclass
from typing import List, Tuple, Dict, Union
import tqdm

DIRECTIONS = [
    (1,0),
    (0,1),
    (-1,0),
    (0,-1)
]

def parse_input(in_lines: List[str]):
    map_rows = in_lines[:-2]
    map_rows = [list(_[:-1]) for _ in map_rows]
    max_col = max([len(_) for _ in map_rows])
    map_rows = [_+[' ']*(max_col-len(_)) for _ in map_rows]

    movements = in_lines[-1]

    movements = re.split("(\d+)", movements.strip())
    movements = movements[1:-1]
    movements = [int(_) if i%2==0 else _ for i,_ in enumerate(movements)]

    return map_rows,movements


def find_in_row(map_rows, row_idx, characters = ".#", reverse=False):
    iterator = enumerate(map_rows[row_idx])
    if reverse:
        iterator = reversed(list(iterator))
    for i,v in iterator:
        if v == characters:
            return i

def move(map_rows, cur_location, direction_idx, steps):
    direction = DIRECTIONS[direction_idx]
    i = 0
    while i < steps:
        n_loc = (cur_location[0]+direction[0], cur_location[1]+direction[1])
        n_loc = ((n_loc[0]+len(map_rows))%len(map_rows), (n_loc[1]+len((map_rows[0])))%len(map_rows[0]))
        print(n_loc, direction, cur_location, len(map_rows))
        if map_rows[n_loc[0]][n_loc[1]] == "#":
            break

        if map_rows[n_loc[0]][n_loc[1]] == ".":
            i += 1
        cur_location = n_loc

    if map_rows[cur_location[0]][cur_location[1]] == " ":
        return move(map_rows, cur_location, (direction_idx+2)%4, 1)

    return cur_location
def solve_first(parsed_input, timelimit=24):
    map_rows, movements = parsed_input
    cur_location = (0, find_in_row(map_rows, 0, "."))
    cur_dir_idx = 1

    for m in movements:
        match m:
            case int():
                print("Move", m)
                cur_location = move(map_rows, cur_location, cur_dir_idx, m)
            case "R":
                cur_dir_idx = (cur_dir_idx-1)%4
            case "L":
                cur_dir_idx = (cur_dir_idx+1)%4


    print(cur_location, cur_dir_idx)
    print((cur_location[0]+1)*1000,4*(cur_location[1]+1),(cur_dir_idx+4-1)%4)
    return (cur_location[0]+1)*1000+4*(cur_location[1]+1)+(cur_dir_idx+4-1)%4

def show(map_rows, cur_location):
    print(cur_location)
    r = copy.deepcopy(map_rows)
    r[cur_location[0]][cur_location[1]] = "A"
    for row in r:
        print(''.join(row))
def move_second(map_rows, cur_location, direction_idx, steps, wraps):
    direction = DIRECTIONS[direction_idx]
    i = 0
    while i < steps:
        new_direction_idx = None
        direction = DIRECTIONS[direction_idx]
        n_loc = (cur_location[0]+direction[0], cur_location[1]+direction[1])


        if not (0 <= n_loc[0] < len(map_rows)) or not (0 <= n_loc[1] < len(map_rows[1])):
            n_loc, new_direction_idx = wraps[n_loc]
        elif map_rows[n_loc[0]][n_loc[1]] == " ":
            # if n_loc not in wraps:
            #     show(map_rows, n_loc)
            n_loc, new_direction_idx = wraps[n_loc]


        if map_rows[n_loc[0]][n_loc[1]] == "#":
            break

        if map_rows[n_loc[0]][n_loc[1]] == ".":
            i += 1
            if new_direction_idx is not None:
                direction_idx = new_direction_idx


        cur_location = n_loc

    return cur_location, direction_idx
def solve_second(parsed_input, step=4):
    map_rows, movements = parsed_input
    cur_location = (0, find_in_row(map_rows, 0, "."))
    cur_dir_idx = 1

    wraps = {}
    if len(map_rows) < 100:
        base = 4
    else:
        base = 50

    def generate_points(top_left, side, size, outside):
        res = []
        outside = int(outside)
        for i in range(size):
            match side:
                case "left":
                    res.append((top_left[0]+i,top_left[1]-outside))
                case "right":
                    res.append((top_left[0] +i, top_left[1] + size-1+outside))
                case "up":
                    res.append((top_left[0]-outside, top_left[1]+i))
                case "down":
                    res.append((top_left[0] +size-1+outside, top_left[1] + i))
        return res
    print(base, len(map_rows), len(map_rows[0]))
    for i in range(0,len(map_rows), base):
        for j in range(0, len(map_rows[0]), base):
            if map_rows[i][j] != " ":
                print("I", end="")
            else:
                print("O", end="")
        print()

    left, right, up, down = [("left", 1), ("right", 3), ("up",0), ("down",2)]
    one = (0, base)
    two = (0, 2*base)
    three = (base, base)
    four = (base*2, base)
    five = (2*base, 0)
    six = (3*base, 0)

    options = [
               (two, down, three, right, False),
                (three, left, five, up, False),
            (two, right, four, right, True),
            (one, left, five, left, True),
            (one, up, six, left, False),
            (two, up, six, down, False),
            (four, down, six, right, False)

               ]
    for a,ad, b, bd, rev in options:
        a_points_out = generate_points(a, ad[0], base, True)
        b_points_in = generate_points(b, bd[0], base, False)
        iterator = zip(a_points_out, b_points_in)
        if rev:
            iterator = zip(a_points_out, reversed(b_points_in))
        for pa, pb in iterator:
            wraps[pa] = (pb, bd[1])

        a_points_in = generate_points(a, ad[0], base, False)
        b_points_out = generate_points(b, bd[0], base, True)

        iterator = zip(a_points_in, b_points_out)
        if rev:
            iterator = zip(a_points_in, reversed(b_points_out))
        for pa, pb in iterator:
            wraps[pb] = (pa, ad[1])


    for i,m in enumerate(movements):


        match m:
            case int():
                # print("Move", m, i, len(movements))
                cur_location, cur_dir_idx = move_second(map_rows, cur_location, cur_dir_idx, m, wraps)
            case "R":
                cur_dir_idx = (cur_dir_idx-1)%4
            case "L":
                cur_dir_idx = (cur_dir_idx+1)%4

    print(cur_location, cur_dir_idx)
    print((cur_location[0] + 1) * 1000, 4 * (cur_location[1] + 1), (cur_dir_idx + 4 - 1) % 4)

    dir_score = {
        0: 1,
        1: 0,
        2: 3,
        3: 2
    }

    return (cur_location[0] + 1) * 1000 + 4 * (cur_location[1] + 1) + dir_score[cur_dir_idx]


if __name__ == '__main__':
    for solver in (
            # solve_first,
            solve_second,
    ):

        with open("input1.txt") as file:
            lines = file.readlines()

        # print("Example res", solver(parse_input(lines)))

        print("Test data")
        with open("input2.txt") as file:
            lines = file.readlines()
        print("Test res", solver(parse_input(lines)))
        print("-"*50)