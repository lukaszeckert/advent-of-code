import itertools

import tqdm
from aocd.examples import Example
from aocd.get import current_day, most_recent_year
from aocd.models import default_user, Puzzle
import os
os.environ["AOC_SESSION"] = "53616c7465645f5f2fc428bfbc698864ca265a1cb242f2644a35b22ffb3eacdc9f7e86272333aae8f94366575482a84792fbc84e14cb2aff0ee698822c380e01"
user = default_user()
day = current_day()
year = most_recent_year()
puzzle = Puzzle(year=year, day=day, user=user)

def push_front(row: list):
    changed = False

    for _ in range(len(row)):
        changed = False
        for i in range(1, len(row)):
            if row[i-1] == "." and row[i] == "O":
                changed = True
                row[i-1], row[i] = row[i], row[i-1]
                row[i-1], row[i] = row[i], row[i-1]

    for _ in range(len(row)):
        changed = False
        for i in range(1, len(row)):
            if row[i-1] == "." and row[i] == "O":
                changed = True
                row[i-1], row[i] = row[i], row[i-1]
        if not changed:
            break

    return row

def solve_a(data: str):
    rows = data.split("\n")
    m = len(rows[0])
    columns = []
    for i in range(m):
        columns.append(push_front([r[i] for r in rows]))

    res = 0
    for col in columns:
        for i,ch in enumerate(reversed(col)):
            if ch == "O":
                res += i+1

    return res
def _cycle(rows):
    n = len(rows)
    m = len(rows[0])
    # North
    columns = [[row[i] for row in rows] for i in range(m)]
    columns = [push_front(_) for _ in columns]
    rows = [[col[i] for col in columns] for i in range(n)]

    # West
    rows = [push_front(_) for _ in rows]

    # South
    columns = [[row[i] for row in rows] for i in range(m)]
    columns = [_[::-1] for _ in columns]
    columns = [push_front(_) for _ in columns]
    columns = [_[::-1] for _ in columns]
    rows = [[col[i] for col in columns] for i in range(n)]

    # East
    rows = [_[::-1] for _ in rows]
    rows = [push_front(_) for _ in rows]
    rows = [_[::-1] for _ in rows]


    return rows
def solve_b(data: str, a):
    rows = data.split("\n")
    seen = dict()
    for _ in range(119-7):
        rows = _cycle(rows)
    # print(1000000000-2-(1000000000-2)//7*7)
    for i in tqdm.tqdm(range(1000000000-112-(1000000000-112)//7*7+21)):
        rows = _cycle(rows)
        cur = ''.join([''.join(_) for _ in rows])
        if cur in seen:
            seen[cur].append(i+1)
            print(i, seen[cur])
        else:
            seen[cur] = [i+1]
    print([len(_) for _ in seen.values()])
    print(len(seen))

    columns = [[row[i] for row in rows] for i in range(len(rows[0]))]
    res = 0
    for col in columns:
        for j,ch in enumerate(reversed(col)):
            if ch == "O":
                res += j+1
        # print(i,res)

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
    #
    # B
    print("Running task B")
    for example in read_examples():
        solved = solve_b(example[0], 1000)
        # print("My solution ", solved, "expected", example[1])
    print(solve_b(puzzle.input_data,150))

if __name__ == '__main__':
    main()