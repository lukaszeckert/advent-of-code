from collections import defaultdict
from functools import reduce

from aocd.examples import Example
from aocd.get import current_day, most_recent_year
from aocd.models import default_user, Puzzle
import os
os.environ["AOC_SESSION"] = "53616c7465645f5f2fc428bfbc698864ca265a1cb242f2644a35b22ffb3eacdc9f7e86272333aae8f94366575482a84792fbc84e14cb2aff0ee698822c380e01"
user = default_user()
day = current_day()
year = most_recent_year()
puzzle = Puzzle(year=year, day=day, user=user)

class HashMap:
    def hash(self, item: str):
        return reduce(lambda a,b: ((a+ord(b))*17)%256, item, 0)
    def insert(self, item, value):
        if item not in self.memory

def hash(code: str):
    res = 0
    for ch in code:
        res = ((res+ord(ch))*17)%256
    return res
def solve_a(data: str):
    codes = data.strip().split(",")
    hashes = list(map(hash, codes))
    return sum(hashes)
def solve_b(data: str):
    codes = data.strip().split(",")
    boxes = defaultdict(list)
    for code in codes:
        if "-" in code:
            code = code.replace("-","")
            code_hash = hash(code)
            boxes[code_hash] = [lens for lens in boxes[code_hash] if lens[0] != code]
        else:
            code, val = code.split("=")
            code_hash = hash(code)
            exists = False
            for lens in boxes[code_hash]:
                if lens[0] == code:
                    exists = True
                    lens[1] = int(val)

            if not exists:
                boxes[code_hash].append([code, int(val)])
    res = 0
    for k,box in boxes.items():
        for i, code in enumerate(box):
            res += (k+1)*(i+1)*code[1]
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

    # B
    print("Running task B")
    for example in read_examples():
        solved = solve_b(example[0])
        print("My solution ", solved, "expected", example[1])
    print(solve_b(puzzle.input_data))

if __name__ == '__main__':
    main()