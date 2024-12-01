import queue
from collections import Counter
from queue import Queue
from typing import List

from aocd.examples import Example
from aocd.get import current_day, most_recent_year
from aocd.models import default_user, Puzzle
import os
os.environ["AOC_SESSION"] = "53616c7465645f5f2fc428bfbc698864ca265a1cb242f2644a35b22ffb3eacdc9f7e86272333aae8f94366575482a84792fbc84e14cb2aff0ee698822c380e01"
user = default_user()
day = current_day()
year = most_recent_year()
puzzle = Puzzle(year=year, day=day, user=user)

class Graf:
    def __init__(self, rows):
        self.rows = [list(_) for _ in rows]

        self.output_directions = {
   # is a vertical pipe connecting north and south.
    '|': (0,2),
    # is a horizontal pipe connecting east and west.
    '-': (3,1),
    # is a 90-degree bend connecting north and east.
    'L': (0,1),
    # is a 90-degree bend connecting north and west.
    'J': (0,3),
    # is a 90-degree bend connecting south and west.
    '7': (2, 3),
    # is a 90-degree bend connecting south and east.
    'F': (2, 1),
    # is ground; there is no pipe in this tile.
    '.': tuple([]),
    # is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
    'S': (0,1,2,3),
    'I': tuple([])
        }

    def output_to_input(self, outputs):
        return tuple([(_+2)%4 for _ in outputs])

    def _can_go(self, start, end, exit_dir):
        if end[0] < 0 or end[1] < 0 or end[0] >= len(self.rows) or end[1] >= len(self.rows[0]):
            return False

        end_dir = self.output_directions[self.rows[end[0]][end[1]]]
        start_dir = self.output_directions[self.rows[start[0]][start[1]]]
        end_rev_dir = self.output_to_input(end_dir)
        if exit_dir in end_rev_dir and exit_dir in start_dir:
            return True
        return False

    def find_loop(self):
        s = find_s(self.rows)

        stack = [s]
        first = True
        visited = set()

        while len(stack) > 0:
            cur = stack.pop()
            if cur == s and not first:
                return True
            first = False
            for i, d in enumerate(
                [(-1,0), (0,1), (1,0), (0,-1)]
            ):
                nc = (cur[0]+d[0], cur[1]+d[1])
                if self._can_go(cur, nc, i):
                    if nc not in visited:
                        stack.append(nc)
                        visited.add(nc)
        return False

    def dfs(self, cur, visited):
        for i, d in enumerate(
                [(-1, 0), (0, 1), (1, 0), (0, -1)]
        ):
            nc = (cur[0] + d[0], cur[1] + d[1])
            if 0 <=nc[0] < len(self.rows) and 0 <= nc[1] < len(self.rows[1]) and nc == (9,2):
                print("Can go", cur, nc, i, self.rows[cur[0]][cur[1]], self.rows[nc[0]][nc[1]], self._can_go(cur, nc, i))
            if self._can_go(cur, nc, i):
                if nc not in visited:
                    # mark everything inside
                    if i == 0:
                        md = (0, 1)
                    if i == 1:
                        md = (1, 0)
                    if i == 2:
                        md = (0, -1)
                    if i == 3:
                        md = (-1, 0)

                    visited[nc] = md
                    self.dfs(nc, visited)

    def solve_2(self):
        s = find_s(self.rows)
        visited= {s: (0,0)}
        self.dfs(s, visited)

        rows = [["I" for _ in range(len(self.rows[0])+2)] for _ in range(len(self.rows)+2)]

        for i,j in visited:
            rows[i+1][j+1] = "X"

        stack = [(0,0)]
        vs = set(stack)
        while stack:
            cur = stack.pop()
            rows[cur[0]][cur[1]] = "O"
            for i, d in enumerate(
                    [(-1, 0), (0, 1), (1, 0), (0, -1)]
            ):
                nc = (cur[0]+d[0], cur[1]+d[1])
                if 0 <= nc[0] < len(rows) and 0 <= nc[1] < len(rows[1]):
                    onc = (nc[0]-1, nc[1]-1)
                    if onc in visited:
                        print(onc, vi)
                    if visited.get(onc) != i and nc not in vs:
                        stack.append(nc)
                        vs.add(nc)


        for row in rows:
            print("".join(row))
        return sum([Counter(_)["I"] for _ in rows])

    def bfs(self):
        s = find_s(self.rows)

        queue = Queue()
        queue.put((s,0))

        distances = {s:0}
        while not queue.empty():
            cur, dis = queue.get()
            distances[cur] = dis
            for i, d in enumerate(
                [(-1,0), (0,1), (1,0), (0,-1)]
            ):
                nc = (cur[0]+d[0], cur[1]+d[1])
                if self._can_go(cur, nc, i):
                    if nc not in distances:
                        queue.put((nc, dis+1))
                        distances[nc] = dis+1
        return max(distances.values())

def find_s(rows: List[str]):
    for i, r in enumerate(rows):
        for j, ch in enumerate(r):
            if ch == "S":
                return i,j
def solve_a(data: str):
    rows = data.split("\n")
    graph = Graf(rows)
    print(graph.find_loop())
    return graph.bfs()

def solve_b(data: str):
    rows = data.split("\n")
    graph = Graf(rows)
    return graph.solve_2()
def main():
    example: Example
    me = [
        ("""..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........""", 4),
#         (""".F----7F7F7F7F-7....
# .|F--7||||||||FJ....
# .||.FJ||||||||L7....
# FJL7L7LJLJ||LJ.L-7..
# L--J.L7...LJS7F-7L7.
# ....F-J..F7FJ|L7L7L7
# ....L7.F7||L7|.L7L7|
# .....|FJLJ|FJ|F7|.LJ
# ....FJL-7.||.||||...
# ....L---J.LJ.LJLJ...""", 8),
#         ("""FF7FSF7F7F7F7F7F---7
# L|LJ||||||||||||F--J
# FL-7LJLJ||||||LJL-77
# F--JF--7||LJLJ7F7FJ-
# L---JF-JLJ.||-FJLJJ7
# |F|F-JF---7F7-L7L|7|
# |FFJF7L7F-JF7|JL---7
# 7-L-JL7||F7|L7F-7F7|
# L.L7LFJ|||||FJL7||LJ
# L7JLJL-JLJLJL--JLJ.L""", 10)
    ]
    # A
    # print("Running task A")
    # for example in me:
    #     solved = solve_a(example[0])
    #     print("My solution ", solved, "expected", example[1])
    # print(solve_a(puzzle.input_data))

    # B
    # print("Running task B")
    # for example in puzzle.examples:
    import sys
    sys.setrecursionlimit(100000)
    for example in me:
        solved = solve_b(example[0])
        print("My solution ", solved, "expected", example[1])
    # print(solve_b(puzzle.input_data))

if __name__ == '__main__':
    main()