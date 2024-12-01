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

def calculate_1d_distances(values: List[int]):
    values.sort()
    cur_sum = 0
    res = 0
    for i, v in enumerate(values):
        res += i*v-cur_sum
        cur_sum += v
    return res

def calculate_1d_expansion(values: List[int], exp_rate=1):
    values.sort()
    res = 0
    for i,(a,b) in enumerate(zip(values, values[1:])):
        diff = max(0,b-a-1)*exp_rate
        res += diff*(i+1)*(len(values)-i-1)
    return res


def solve_a(data: str):
    data = data.split("\n")
    gal = []
    for i,row in enumerate(data):
        for j, ch in enumerate(row):
            if ch == "#":
                gal.append((i,j))

    gal_distance = calculate_1d_distances([_[0] for _ in gal])
    gal_distance += calculate_1d_distances([_[1] for _ in gal])

    expansion_distances = calculate_1d_expansion([_[0] for _ in gal])
    expansion_distances += calculate_1d_expansion([_[1] for _ in gal])
    return gal_distance+expansion_distances
def solve_b(data: str):
    data = data.split("\n")
    gal = []
    for i,row in enumerate(data):
        for j, ch in enumerate(row):
            if ch == "#":
                gal.append((i,j))

    gal_distance = calculate_1d_distances([_[0] for _ in gal])
    gal_distance += calculate_1d_distances([_[1] for _ in gal])

    expansion_distances = calculate_1d_expansion([_[0] for _ in gal], 999_999)
    expansion_distances += calculate_1d_expansion([_[1] for _ in gal], 999_999)
    return gal_distance+expansion_distances


# 842645913794

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
    print(solve_b(puzzle.input_data))

if __name__ == '__main__':
    main()