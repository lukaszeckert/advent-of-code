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
    pass

def solve_b(data: str):
    pass

def read_examples():
    with open("example.txt") as file:
        content = file.read()

    values = content.split("!---!")
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