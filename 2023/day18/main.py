import functools
from dataclasses import dataclass
from itertools import chain

from aocd.examples import Example
from aocd.get import current_day, most_recent_year
from aocd.models import default_user, Puzzle
import os
os.environ["AOC_SESSION"] = "53616c7465645f5f2fc428bfbc698864ca265a1cb242f2644a35b22ffb3eacdc9f7e86272333aae8f94366575482a84792fbc84e14cb2aff0ee698822c380e01"
user = default_user()
day = current_day()
year = most_recent_year()
puzzle = Puzzle(year=year, day=day, user=user)

@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int
    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def __mul__(self, other: float):
        return Point(self.x * other, self.y * other)
@dataclass
class Line:
    start: Point
    end: Point

DIRECTIONS ={
    "R": Point(1,0),
    "L": Point(-1,0),
    "D": Point(0,1),
    "U": Point(0,-1)
}
def right_direction(point: Point) -> Point:
    match point:
        case Point(1,0):
            return Point(0,1)
        case Point(0,1):
            return Point(-1,0)
        case Point(-1,0):
            return Point(0,-1)
        case Point(0,-1):
            return Point(1,0)

def draw(vis):
    min_x, min_y, max_x, max_y = min([_.x for _ in vis]),min([_.y for _ in vis]),max([_.x for _ in vis]),max([_.y for _ in vis])

    grid = [["." for _ in range(max_x-min_x+1)] for _ in range(max_y-min_y+1)]

    for v in vis:
        grid[v.y - min_y][v.x - min_x] = "#"

    for line in grid:
        print(''.join(line))


def solve_a(data: str):

    cur = Point(0,1)
    visited = set([cur])
    lines = data.split("\n")
    for line in lines:
        direction, steps, color = line.strip().split()
        direction = DIRECTIONS[direction]

        for _ in range(int(steps)):
            cur = cur + direction
            visited.add(cur)

    cur = Point(0,1)
    new_visited = set([cur])
    for line in lines:
        direction, steps, color = line.strip().split()
        direction = DIRECTIONS[direction]

        for _ in range(int(steps)):
            cur = cur + direction
            new_visited.add(cur)
            right = right_direction(direction)
            nd = cur+right
            while nd not in visited:
                new_visited.add(nd)
                nd += right

    draw(new_visited)
    return len(new_visited)

def solve_b(data: str):
    lines = data.split("\n")


    instructions = []
    for line in lines:
        # direction, steps, color = line.strip().split()
        # direction = DIRECTIONS[direction]
        # steps = int(steps)
        # instructions.append((direction, steps))

        _,_, line = line.strip().split(" ")
        line = line[2:-1]
        steps = int(line[:5], 16)
        sdirection = line[-1]
        match sdirection:
            case "0":
                direction = "R"
            case "1":
                direction = "D"
            case "2":
                direction = "L"
            case "3":
                direction = "U"

        direction = DIRECTIONS[direction]
        instructions.append((direction, steps))
    res = 0
    cur_point = Point(1,1)
    trench_lines = []

    aaa = [cur_point]
    for i,instruction in enumerate(instructions):
        direction, steps = instruction
        next_point = cur_point + direction*int(steps)
        aaa.append(next_point)
        res += steps

        prev_direction = instructions[i-1][0]
        next_direction = instructions[(i+1)%len(instructions)][0]

        line_start = cur_point
        line_end = next_point

        height = abs(line_start.y-line_end.y)+1
        if right_direction(prev_direction) == direction:
            line_start = line_start+direction
            height -= 1
        if right_direction(direction) == next_direction:
            line_end = line_end + direction*-1
            height -= 1

        if direction.y != 0 and height > 0:
            if line_start.y <= line_end.y:
                trench_lines.append(Line(line_start, line_end))
            elif line_start.y > line_end.y:
                trench_lines.append(Line(line_end, line_start))

        cur_point = next_point

    print(aaa)
    res2 = 0
    for a,b in zip(aaa, aaa[1:]):
        res2 += a.x*b.y-a.y*b.x
    return abs(res2) //2 + res//2 +1


    if len(trench_lines):
        cur_y = min([line.start.y for line in trench_lines])
        max_y = max([line.end.y for line in trench_lines])+1
        min_y = min([line.start.y for line in trench_lines])
        all_ends = [line.end.y for line in trench_lines] + [line.start.y for line in trench_lines]
        all_ends = [[_-1,_,_+1] for _ in all_ends]
        all_ends = chain.from_iterable(all_ends)
        all_ends = sorted(set(all_ends))[::-1]
        while True:
            # 129849166997110
            lines = [line for line in trench_lines if line.start.y <= cur_y <= line.end.y]
            if len(lines) == 0:
                break
            ncur_y = all_ends.pop()
            height = ncur_y-cur_y+1
            lines = sorted(lines, key=lambda x: x.end.x)
            for p,n in zip(lines[::2], lines[1::2]):
                res += height*(n.start.x-p.start.x-1)

            cur_y = ncur_y+1

    return res




def read_examples():
    with open("example.txt") as file:
        content = file.read()

    values = content.split("\n!---!\n")
    return [_ for _ in zip(values[0::2], values[1::2])]


def main():
    # A
    # print("Running task A")
    # for example in read_examples():
    #     solved = solve_a(example[0])
    #     print("My solution ", solved, "expected", example[1])
    # print(solve_a(puzzle.input_data))

    # B
    print("Running task B")
    for example in read_examples():
        solved = solve_b(example[0])
        print("My solution ", solved, "expected", example[1])
    print(solve_b(puzzle.input_data))

if __name__ == '__main__':
    main()