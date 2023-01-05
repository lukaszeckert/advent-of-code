import functools
import itertools
import operator
import re
import struct
from dataclasses import dataclass
from typing import List, Tuple, Dict
import tqdm
@dataclass(eq=True, unsafe_hash=True)
class Point:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y, self.z+other.z)

def parse_input(in_lines: List[str]):
    points = [Point(*map(int,_.strip().split(","))) for _ in in_lines]
    print(points)
    return points

def solve_first(parsed_input):
    points = parsed_input
    seen = {*points}
    res = 0
    for p in points:
        for d in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0), (0,0,1), (0,0,-1)]:
            point_d = Point(*d)
            if p+point_d not in seen:
                res += 1
    return res
def solve_second(parsed_input):

    points = {*parsed_input}
    visited = {}
    counts = {}
    waters = {}
    edge_min = Point(x=min([_.x for _ in points])-2,
                     y=min([_.y for _ in points])-2,
                     z=min([_.z for _ in points])-2,
                     )
    edge_max = Point(x=max([_.x for _ in points])+2,
                     y=max([_.y for _ in points])+2,
                     z=max([_.z for _ in points])+2,
                     )

    start = set()
    res = 0
    for p in points:
        for d in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            point_d = Point(*d)
            if p + point_d not in points:
                start.add(p+point_d)

    def dfs(point, color):
        nonlocal res
        if point in points:
            counts[color] = counts.get(color,0)+1
            return

        if point in visited:
            return



        if not (edge_min.x < point.x < edge_max.x) or not (edge_min.y < point.y < edge_max.y) or not (edge_min.z < point.z < edge_max.z):
            waters[color] = True
            return

        visited[point] = color
        for d in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            point_d = Point(*d)
            if point_d+point in points:
                res += 1


            dfs(point+point_d, color)

    dfs(edge_min+Point(1,1,1), 0)
    return counts[0],res



    return res

if __name__ == '__main__':
    for solver in (
            #solve_first,
            solve_second,
    ):
        import sys
        sys.setrecursionlimit(10000)
        with open("input1.txt") as file:
            lines = file.readlines()

        print("Example res", solver(parse_input(lines)))

        print("Test data")
        with open("input2.txt") as file:
            lines = file.readlines()
        print("Test res", solver(parse_input(lines)))
