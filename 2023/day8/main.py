from dataclasses import dataclass

from aocd.examples import Example
from aocd.get import current_day, most_recent_year
from aocd.models import default_user, Puzzle
import os
os.environ["AOC_SESSION"] = "53616c7465645f5f2fc428bfbc698864ca265a1cb242f2644a35b22ffb3eacdc9f7e86272333aae8f94366575482a84792fbc84e14cb2aff0ee698822c380e01"
user = default_user()
day = current_day()
year = most_recent_year()
puzzle = Puzzle(year=year, day=day, user=user)
@dataclass
class Row:
    start: str
    to: list

    @property
    def left(self):
        return self.to[0]

    @property
    def right(self):
        return self.to[1]

def solve_a(data: str):
    start, other = data.split("\n\n")
    start: str = start.strip()
    other = other.split("\n")
    other = [_.strip().replace(" ", "").replace("(", "").replace(")", "").split("=") for _ in other]
    rows = [Row(_[0], _[1].split(",")) for _ in other]
    rows = {_.start: _ for _ in rows}
    cur = "AAA"
    pos = 0
    while cur != "ZZZ":
        side = start[pos%len(start)]
        if side == "L":
            cur = rows[cur].left
        else:
            cur = rows[cur].right
        pos += 1
    return pos

def solve_b(data: str):

    start, other = data.split("\n\n")
    start: str = start.strip()
    other = other.split("\n")
    other = [_.strip().replace(" ", "").replace("(", "").replace(")", "").split("=") for _ in other]
    rows = [Row(_[0], _[1].split(",")) for _ in other]
    rows = {_.start: _ for _ in rows}
    a: str
    res = float("inf")
    starting = [_ for _ in rows.keys() if _.endswith("A")]

    cur = starting
    pos = 0
    while not all([_.endswith("Z") for _ in cur]):
        if pos % 1000 == 0:
            print(pos, cur)
        side = start[pos%len(start)]
        if side == "L":
            cur = [rows[c].left for c in cur]
        else:
            cur = [rows[c].right for c in cur]
        pos += 1
    return pos

def solve_b2(data: str):

    start, other = data.split("\n\n")
    start: str = start.strip()
    other = other.split("\n")
    other = [_.strip().replace(" ", "").replace("(", "").replace(")", "").split("=") for _ in other]
    rows = [Row(_[0], _[1].split(",")) for _ in other]
    rows = {_.start: _ for _ in rows}
    a: str
    res = float("inf")
    starting = [_ for _ in rows.keys() if _.endswith("A")]

        #["VCA", "GLZ"]
    poss = []
    for st in starting:
        pos = 0
        visited = []
        cur = (pos%len(start), st)


        while cur not in visited:
            if cur[1].endswith("Z"):
                visited.append(cur)
            side = start[pos % len(start)]
            if side == "L":
                cur_s = rows[cur[1]].left
            else:
                cur_s = rows[cur[1]].right
            pos += 1
            cur = (pos%len(start), cur_s)
        # print(pos, cur, pos%len(start), len(start))

        visited.append(cur)
        print(st, pos, visited)
        poss.append(pos)
    def nwd(a,b):
        if b > 0:
            return nwd(b, a%b)
        return a

    def nww(a,b):
        return a*b//nwd(a,b)

    cur = 1
    for p in poss:
        cur = nww(cur, p//2)
    return cur

def main():
    example: Example
    # A
    print("Running task A")
    # for example in puzzle.examples:
    #     solved = solve_a(example.input_data)
    #     print("My solution ", solved, "expected", example.answer_a)
    # print(solve_a(puzzle.input_data))

    # B
    print("Running task B")
#     for example in puzzle.examples:
#         solved = solve_b(example.input_data)
#         print("My solution ", solved, "expected", example.answer_b)
    st = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    print(solve_b2(st))
    print(solve_b2(puzzle.input_data))

if __name__ == '__main__':
    main()