from dataclasses import dataclass
from typing import List

import tqdm
from aocd.examples import Example
from aocd.get import current_day, most_recent_year
from aocd.models import default_user, Puzzle
import os

os.environ[
    "AOC_SESSION"] = "53616c7465645f5f2fc428bfbc698864ca265a1cb242f2644a35b22ffb3eacdc9f7e86272333aae8f94366575482a84792fbc84e14cb2aff0ee698822c380e01"
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


class Empty:
    def __call__(self, point: "Point", dir: Point) -> List[Point]:
        return [(point + dir, dir)]


class Mirror:
    def __init__(self, val: str):
        self.val = val

    def __call__(self, point: Point, dir: Point) -> List[ Point ]:
        if self.val == "\\":
            nd = Point(dir.y, dir.x)
            return [(point+nd, nd)]
        nd = Point(-dir.y, -dir.x)
        return [(point+nd, nd)]

class Spliter:
    def __init__(self, val: str):
        self.val = val

    def __call__(self, point: "Point", dir: Point) -> List[Point]:
        if (self.val == "|" and dir in (Point(0, 1), Point(0, -1))
                or self.val == "-" and dir in (Point(1, 0), Point(-1, 0))):
            return [(point + dir, dir)]
        if self.val == "|":
            nd1 = Point(0,1)
            nd2 = Point(0,-1)
            return [(point+nd1, nd1), (point+nd2, nd2)]
        nd1 = Point(1,0)
        nd2 = Point(-1,0)
        return [(point + nd1, nd1), (point + nd2, nd2)]

def build(char: str):
    match char:
        case ".":
            return Empty()
        case "\\" | "/":
            return Mirror(char)
        case "-" | "|":
            return Spliter(char)
def solve_a(data: str, start_pos= Point(0,0), start_dir= Point(1,0)):
    data = data.split("\n")
    rows = []
    for row in data:
        row = [build(_) for _ in row]
        rows.append(row)
    n,m = len(rows), len(rows[0])


    stack = [(start_pos, start_dir)]
    visited = set(stack)

    while stack:
        cur_point, direction = stack.pop()
        next_points = rows[cur_point.y][cur_point.x](cur_point, direction)
        for next_point in next_points:
            if next_point not in visited and 0 <= next_point[0].x < m and 0 <= next_point[0].y < n:
                stack.append(next_point)
                visited.add(next_point)

    return len({k[0] for k in visited})
def solve_b(data: str):
    rows = data.split("\n")
    n = len(rows)
    m = len(rows[0])
    res = 0
    for i in tqdm.tqdm(range(n)):
        res = max(res, solve_a(data, Point(0, i), Point(1,0)))
        res = max(res, solve_a(data, Point(m-1, i), Point(-1,0)))

    for i in tqdm.tqdm(range(m)):
        res = max(res, solve_a(data, Point(i, 0), Point(0,1)))
        res = max(res, solve_a(data, Point(i, n-1), Point(0,-1)))

    return res

def read_examples():
    with open("example.txt") as file:
        content = file.read()

    values = content.split("\n!---!\n")
    return [_ for _ in zip(values[0::2], values[1::2])]


def main():
    # A
    print("Running task A")
    for example in read_examples():
        solved = solve_a(example[0])
        print("My solution ", solved, "expected", example[1])
    print(solve_a(puzzle.input_data))

    # B
    print("Running task B")
    for example in read_examples():
        solved = solve_b(example[0])
        print("My solution ", solved, "expected", example[1])
    print(solve_b(puzzle.input_data))


if __name__ == '__main__':
    main()
