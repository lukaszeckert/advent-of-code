from math import floor, ceil

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
    times, distances = data.split("\n")
    times = [int(_) for _ in times.split(":")[1].split()]
    distances = [int(_) for _ in distances.split(":")[1].split()]

    res = 1
    for time, distance in zip(times, distances):
        cur = 0
        for i in range(time):
            if i*(time-i) > distance:
                cur += 1
        print(time, distance, cur)
        res *= cur
    return res
def solve_b(data: str):

    times, distances = data.split("\n")
    time = int(times.split(":")[1].replace(" ", "").strip())
    distance = int(distances.split(":")[1].replace(" ", "").strip())
    res = 1
    cur = 0
    for i in range(time):
        if i * (time - i) > distance:
            cur += 1
    res *= cur
    return res

def solve_b2(data: str):

    times, distances = tuple(data.split("\n"))
    time = int(times.split(":")[1].replace(" ", "").strip())
    distance = int(distances.split(":")[1].replace(" ", "").strip())
    a = -1
    for i, distance in enumerate(distances):
        pass
    for i, distance in enumerate(distances):
        pass


    b = time
    c = -distance
    left = (-b+(b**2-4*a*c)**(1/2))/(2*a)
    right = (-b - (b ** 2 - 4 * a * c) ** (1 / 2)) / (2 * a)
    return -ceil(left)+floor(right)+1

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
        solved = solve_b2(example.input_data)
        print("My solution ", solved, "expected", example.answer_b)
    print(solve_b2(puzzle.input_data))

if __name__ == '__main__':
    main()