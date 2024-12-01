from collections import deque

from aocd.examples import Example
from aocd.get import current_day, most_recent_year
from aocd.models import default_user, Puzzle
import os
os.environ["AOC_SESSION"] = "53616c7465645f5f2fc428bfbc698864ca265a1cb242f2644a35b22ffb3eacdc9f7e86272333aae8f94366575482a84792fbc84e14cb2aff0ee698822c380e01"
user = default_user()
day = current_day()
year = most_recent_year()
puzzle = Puzzle(year=year, day=day, user=user)
def solve(data: str, max_distance):
    rows = data.split("\n")
    n, m = len(rows), len(rows[0])

    s = (0, 0)
    for i, row in enumerate(rows):
        for j, ch in enumerate(row):
            if ch == "S":
                s = (i, j)

    visited = {}
    queue = deque([(s, 0)])
    while queue:
        cur, dist = queue.popleft()
        key = (dist % 2, cur)
        if key in visited or dist > max_distance:
            continue

        visited[key] = dist

        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = cur[0] + dy, cur[1] + dx
            if 0 <= ny < n and 0 <= nx < m and rows[ny][nx] in [".", "S"]:
                queue.append(((ny, nx), dist + 1))

    return visited

def solve_a(data: str, max_distance=6, goal=0):
    visited = solve(data, max_distance)
    return len([_ for _ in visited.keys() if _[0] == 0])


def mod(a, b):
    while a < 0:
        a += b
    return a%b
def solve_b(data: str):
    G = {i + j * 1j: c for i, r in enumerate(open("full.txt"))
         for j, c in enumerate(r) if c in '.S'}
    N = 131
    done = []
    todo = {x for x in G if G[x] == 'S'}
    for s in range(int(2.5 * N) + 1):
        if s == 64: print(len(todo))
        if s % N == N // 2: done.append(len(todo))

        todo = {p + d for d in {1, -1, 1j, -1j} for p in todo
                if (p + d).real % N + (p + d).imag % N * 1j in G}

    f = lambda n, a, b, c: a + n * (b - a) + n * (n - 1) // 2 * ((c - b) - (b - a))
    print(f(26501365 // N, *done))
    print('aaaa')
    max_distance = 26501365
    # max_distance = 1000
    rows = data.split("\n")
    n,m = len(rows), len(rows[0])
    center_solve = solve(data, max_distance=float("inf"))
    odd = len([_ for _ in center_solve if _[0] == 0])
    even = len([_ for _ in center_solve if _[0] == 1])


    full_solve_center = max([v for k,v in solve(data, max_distance=float("inf")).items() if k[0] == 1])
    print("Max distance for full solve", full_solve_center)
    print(odd, even)

    # Steps needed to reach new square: (dis_x+dis_y)*131 where dis_x and dis_y are square number in x and y

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
    print(solve_a(puzzle.input_data, max_distance=64))

    # B
    print("Running task B")
    for example in read_examples():
        solved = solve_b(example[0])
        print("My solution ", solved, "expected", example[1])
    print(solve_b(puzzle.input_data))

if __name__ == '__main__':
    main()