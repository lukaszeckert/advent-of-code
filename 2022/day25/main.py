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
    blizzards = []
    walls = []
    player = []
    exit_pos = []

    for i,line in enumerate(in_lines):
        line = line.strip()
        for j,ch in enumerate(line):
            match ch:
                case ".":
                    if i == 0:
                        player = Vec2(j,i)
                    if i == len(in_lines)-1:
                        exit_pos = Vec2(j,i)
                case ">":
                    blizzards.append(Blizzard(Vec2(j,i), EAST))
                case "<":
                    blizzards.append(Blizzard(Vec2(j,i), WEST))
                case "^":
                    blizzards.append(Blizzard(Vec2(j,i), NORTH))
                case "v":
                    blizzards.append(Blizzard(Vec2(j,i), SOUTH))
                case "#":
                    walls.append(Vec2(j,i))

    return blizzards, walls, player, exit_pos, len(in_lines), len(in_lines[0].strip())



def move(blizzards: Dict[Vec2, List[Blizzard]], n, m):
    res = {}
    for key in blizzards.values():
        for b in key:
            new_b = Blizzard(b.pos+b.direction, b.direction)
            if new_b.pos.y == 0:
                new_b.pos = Vec2(y=n-2, x=new_b.pos.x)
            if new_b.pos.y == n-1:
                new_b.pos = Vec2(y=1, x=new_b.pos.x)
            if new_b.pos.x == 0:
                new_b.pos = Vec2(x=m - 2, y=new_b.pos.y)
            if new_b.pos.x == m-1:
                new_b.pos = Vec2(x=1, y=new_b.pos.y)
            row = res.get(new_b.pos, list())
            row.append(new_b)
            res[new_b.pos] = row

    return res

def show(blizards, n, m):

    res = [["." for _ in range(m)] for _ in range(n)]

    for k in blizards.values():
        for b in k:

            res[b.pos.y][b.pos.x] = "B"

    for r in res:
        print(''.join(r))
def solve_first(parsed_input, num_iter=10):

    walls: List[Vec2]
    player: Vec2
    exit_pos: Vec2

    blizzards, walls, player, exit_pos, n, m = parsed_input
    blizzards = {_.pos:[_] for _ in blizzards}

    move({'a': [Blizzard(Vec2(1, 1), Vec2(1, 0))]}, n, m)
    queue = [(player,0)]
    queue_poz = 0
    cur_map_minute = 0
    visited = set()

    while queue_poz < len(queue):
        cur: Vec2
        cur, cur_min = queue[queue_poz]
        queue_poz += 1
        if cur_min > cur_map_minute:

            blizzards = move(blizzards, n, m)
            # if cur_min % 100 == 0:
            #     show(blizzards, n, m)
            #     print(blizzards)

            cur_map_minute = cur_min

        if cur.y < 0:
            continue
        if cur in blizzards:
            continue
        if cur in walls:
            continue

        if cur == exit_pos:
            return cur_min

        for m_d in [NORTH, SOUTH, WEST, EAST, Vec2(0,0)]:
            if not (cur+m_d, cur_min+1) in visited:
                visited.add(((cur+m_d, cur_min+1)))
                queue.append((cur+m_d, cur_min+1))


def solve_second(parsed_input, step=4):
    walls: List[Vec2]
    player: Vec2
    exit_pos: Vec2

    blizzards, walls, player, exit_pos, n, m = parsed_input
    blizzards = {_.pos: [_] for _ in blizzards}

    cur_map_minute = 0
    cur_min = 0

    for start, finish in tqdm.tqdm([(player, exit_pos), (exit_pos, player), (player, exit_pos)]):
        queue = [(start, cur_min)]
        queue_poz = 0

        visited = set()

        while queue_poz < len(queue):
            cur: Vec2
            cur, cur_min = queue[queue_poz]
            queue_poz += 1
            if cur_min > cur_map_minute:
                blizzards = move(blizzards, n, m)
                cur_map_minute = cur_min

            if cur.y < 0 or cur.y >= n:
                continue
            if cur in blizzards:
                continue
            if cur in walls:
                continue

            if cur == finish:
                break

            for m_d in [NORTH, SOUTH, WEST, EAST, Vec2(0, 0)]:
                if not (cur + m_d, cur_min + 1) in visited:
                    visited.add(((cur + m_d, cur_min + 1)))
                    queue.append((cur + m_d, cur_min + 1))

    return cur_min


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
        print("-"*50)