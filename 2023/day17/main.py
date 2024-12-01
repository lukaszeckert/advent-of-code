import heapq
from dataclasses import dataclass
from queue import PriorityQueue
from typing import NamedTuple
import numpy as np
from aocd.examples import Example
from aocd.get import current_day, most_recent_year
from aocd.models import default_user, Puzzle
import os
os.environ["AOC_SESSION"] = "53616c7465645f5f2fc428bfbc698864ca265a1cb242f2644a35b22ffb3eacdc9f7e86272333aae8f94366575482a84792fbc84e14cb2aff0ee698822c380e01"
user = default_user()
day = current_day()
year = most_recent_year()
puzzle = Puzzle(year=year, day=day, user=user)

def point_factory(x,y):
    return x+(y<<16)

def point_x(val):
    return val & ((2<<15)-1)
def point_y(val):
    return val >> 16

# @dataclass(eq=True, frozen=True, slots=True)
class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

DIRECTIONS = [
    Point(0,1), Point(1,0), Point(-1,0), Point(0,-1)
]

def solve_a(data: str):
    rows = data.split("\n")
    rows = [list(map(int, row)) for row in rows]
    n,m = len(rows), len(rows[0])

    priority_queue = PriorityQueue()
    priority_queue.put((0, 0, Point(0,0),Point(0,0)))
    completed = dict()

    while not priority_queue.empty():
        dist, straight, direction, point = priority_queue.get()
        key = (point, direction, straight)
        if key in completed:
            continue
        completed[key] = dist

        for dir in DIRECTIONS:
            if abs(dir.x -direction.x) == 2 or abs(dir.y-direction.y) == 2:
                # Reverse
                continue
            np =point+dir
            if not (0 <= np.x < m and 0 <= np.y < n):
                continue

            nstraight = 1

            ndist = dist + rows[np.y][np.x]
            if dir == direction:
                nstraight = straight + 1
            if nstraight > 3:
                continue

            priority_queue.put((ndist, nstraight, dir, np))
    res = min([v for k,v in completed.items() if k[0] == Point(m-1, n-1)])
    return res
def solve_b(data: str):
    rows = data.split("\n")
    rows = [list(map(int, row)) for row in rows]
    n, m = len(rows), len(rows[0])


    priority_queue = PriorityQueue()
    priority_queue.put([(0, 0, Point(0, 0), Point(0, 0))])
    completed = dict()

    while not priority_queue.empty():
        dist, straight, direction, point = priority_queue.get()
        key = (point, direction, straight)
        if key in completed:
            continue
        completed[key] = dist

        for dir in DIRECTIONS:
            if abs(dir.x - direction.x) == 2 or abs(dir.y - direction.y) == 2:
                # Reverse
                continue
            np = point + dir
            if not (0 <= np.x < m and 0 <= np.y < n):
                continue

            nstraight = 1

            ndist = dist + rows[np.y][np.x]
            if dir == direction:
                nstraight = straight + 1
                if nstraight > 10:
                    continue
            elif straight < 4 and direction != Point(0,0):
                    continue


            priority_queue.put((ndist, nstraight, dir, np))
    res = min([v for k, v in completed.items() if k[0] == Point(m - 1, n - 1) and k[2] >= 4])
    return res

def solve_bv2(data: str, min_moves = 0, max_moves = 3):
    rows = data.split("\n")
    rows = [list(map(int, row)) for row in rows]
    n, m = len(rows), len(rows[0])


    priority_queue = [(0, Point(0, 0), Point(0, 0))]
    completed = dict()

    while len(priority_queue):
        dist, direction, point = heapq.heappop(priority_queue)
        key = (point, direction)

        if completed.get(key, float("inf")) < dist:
            continue
        # completed[key] = dist

        if point == Point(m - 1, n - 1):
            break

        for dir in DIRECTIONS:
            if abs(dir.x - direction.x) == 2 or abs(dir.y - direction.y) == 2 or dir == direction:
                # Reverse and the same direction
                continue
            delta_dist = 0
            np = point
            for i in range(max_moves):
                np = np + dir
                if not (0 <= np.x < m and 0 <= np.y < n):
                    break
                delta_dist += rows[np.y][np.x]
                ndist = dist + delta_dist
                if i >= min_moves and completed.get((np, dir), float("inf")) > ndist:
                    heapq.heappush(priority_queue, (ndist, dir, np))
                    completed[(np, dir)] = min(completed.get((np, dir), float("inf")), ndist)

    res = min([v for k, v in completed.items() if k[0] == Point(m - 1, n - 1)])
    return res


def solve_bv3(data: str, min_moves = 0, max_moves = 3):
    rows = data.split("\n")
    rows = [list(map(int, row)) for row in rows]
    n, m = len(rows), len(rows[0])


    priority_queue = [(0, -1, 0)]
    completed = np.zeros((4, n, m))
    completed[:] = float("inf")

    while len(priority_queue):
        dist, direction, point = heapq.heappop(priority_queue)
        key = (point, direction)

        if completed.get(key, float("inf")) < dist:
            continue
        if point == point_factory(m - 1, n - 1):
            break

        for dir in [point_factory(0,1), point_factory(0, -1), point_factory(1,0), point_factory(-1,0)]:
            if abs(point_x(dir) - point_x(direction)) == 2 or abs(point_y(dir) - point_y(direction)) == 2 or dir == direction:
                # Reverse and the same direction
                continue
            delta_dist = 0
            np = point
            for i in range(max_moves):
                np = np + dir
                if not (0 <= point_x(np) < m and 0 <= point_y(np) < n):
                    break
                delta_dist += rows[point_y(np)][point_x(np)]
                ndist = dist + delta_dist

                if i >= min_moves and completed.get((np, dir), float("inf")) > ndist:
                    heapq.heappush(priority_queue, (ndist, dir, np))
                    completed[(np, dir)] = ndist

    res = min([v for k, v in completed.items() if k[0] == point_factory(m - 1, n - 1)])
    return res
def read_examples():
    with open("example.txt") as file:
        content = file.read()

    values = content.split("\n!---!\n")
    return [_ for _ in zip(values[0::2], values[1::2])]


def main():
    # # A
    print("Running task A")
    for example in read_examples():
        solved = solve_bv2(example[0], 0, 3)
        print("My solution ", solved, "expected", example[1])
    # print(solve_a(puzzle.input_data))

    # B
    print("Running task B")
    for example in read_examples():
        # solved = solve_b(example[0])
        # solvedv2 = solve_bv2(example[0], 3,10)
        solvedv2 = None
        solvedv3 = solve_bv3(example[0], 3,10)
        print("My solution ", solvedv2, solvedv3, "expected", example[1])
    # print(solve_b(puzzle.input_data))

if __name__ == '__main__':
    main()