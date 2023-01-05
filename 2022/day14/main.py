import itertools
import operator
import struct
from dataclasses import dataclass
from typing import List

@dataclass
class Line:
    start_x: int
    start_y: int
    end_x: int
    end_y: int

    def __post_init__(self):
        self.start_x, self.end_x = sorted([self.start_x, self.end_x])
        self.start_y, self.end_y = sorted([self.start_y, self.end_y])


    def is_vertical(self):
        if self.start_x == self.end_x:
            return True
        return False

    def is_horizontal(self):
        return self.start_y == self.end_y


def solve(in_lines: List[str]):
    in_lines = [_.strip() for _ in in_lines]
    in_lines = [_.split("->") for _ in in_lines]

    lines = []
    for row in in_lines:
        prev = None
        for ch in row:
            point = [int(_.strip()) for _ in ch.split(",")]
            if prev:
                lines.append(Line(*prev, *point))
            prev = point

    sands = set()
    for line in lines:
        if line.is_vertical():
            for y in range(line.start_y, line.end_y+1):
                sands.add((line.start_x, y))
        else:
            for x in range(line.start_x, line.end_x + 1):
                sands.add((x, line.start_y))

    max_y = max([_[1] for _ in sands])+2
    for i in range(-20000, 20000):
        sands.add((i,max_y))
    i = 0
    while (500, 0) not in sands:

        cur_pos = (500,0)
        while cur_pos[1] <= max_y:
            for dx,dy in ((0,1), (1,1), (-1,1)):
                if not ((cur_pos[0]+dx, cur_pos[1]+dy)) in sands:
                    cur_pos = ((cur_pos[0]+dx, cur_pos[1]+dy))
                    break
            else:
                break

        else:
            break

        sands.add(cur_pos)
        i += 1

    return i

def flow(pos, walls_sand, bottom):


def solve(lines):
    walls_sand = set()
    for line in lines:
        for (x1,y1),(x2,y2) in itertools.pairwise([tuple(map(int, _.strip().split(","))) for _ in line.split("->")]):
            walls_sand |= {*itertools.product(range(min(x1, x2), max(x1, x2) + 1), range(min(y1, y2), max(y1, y2) + 1))}

    bottom = min([_[1] for _ in walls_sand])

    while (500, 0) not in walls_sand:
        end_pos = flow((500,-1))
        walls_sand.add(end_pos)



if __name__ == '__main__':
    with open("input1.txt") as file:
        lines = file.readlines()
    print("Example res", solve(lines))

    print("Test data")
    with open("input2.txt") as file:
        lines = file.readlines()
    # print("Test res", solve(lines))


