import re
from collections import defaultdict
from queue import PriorityQueue

from aocd.examples import Example
from aocd.get import current_day, most_recent_year
from aocd.models import default_user, Puzzle
import os
os.environ["AOC_SESSION"] = "53616c7465645f5f2fc428bfbc698864ca265a1cb242f2644a35b22ffb3eacdc9f7e86272333aae8f94366575482a84792fbc84e14cb2aff0ee698822c380e01"
user = default_user()
day = current_day()
year = most_recent_year()
puzzle = Puzzle(year=year, day=day, user=user)
def solve_a(data: str):
    lines = data.split("\n")
    res = 0
    for line in lines:
        _,line = line.split(":")
        w,l = line.split("|")
        w = set([int(_) for _ in w.strip().split(" ") if _ != ''])
        l = set([int(_) for _ in l.strip().split(" ") if _ != ''])
        common = w & l
        res += (2**len(common))//2
    return res
def solve_b(data: str):
    queue = PriorityQueue()
    cur_count = 0

    lines = data.split("\n")
    res = 0
    for i,line in enumerate(lines):
        id_,line = line.split(":")
        w,l = line.split("|")
        w = set(map(int, w.split()))
        l = set(map(int, l.split()))

        common = len(w & l)
        while not queue.empty():
            row, row_count = queue.get()
            if row >= i:
                queue.put((row, row_count))
                break
            cur_count -= row_count

        res += 1 + cur_count
        if common > 0:
            queue.put((i+common, cur_count+1))
            cur_count += cur_count+1
    return res

def main():
    example: Example
    # A
    # print("Running task A")
    # for example in puzzle.examples:
    #     solved = solve_a(example.input_data)
    #     print("My solution ", solved, "expected", example.answer_a)
    # print(solve_a(puzzle.input_data))

    # B
    print("Running task B")
    for example in puzzle.examples:
        solved = solve_b(example.input_data)
        print("My solution ", solved, "expected", example.answer_b)
    # print(solve_b(puzzle.input_data))

if __name__ == '__main__':
    main()