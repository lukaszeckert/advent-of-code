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
class Row:
    def __init__(self, row:str, numbers, two=False):
        multi = 1
        if two:
            multi = 5
        self.row = "." + '?'.join([row] * multi) + "."
        self.number = numbers * multi
        self.cache = {}

    def solve(self, row_pos = 0, num_pos = 0):
        if num_pos >= len(self.number):
            return all([_ in (".", "?") for _ in self.row[row_pos:]])
        cur_number = self.number[num_pos]

        if row_pos >= len(self.row):
            return 0

        # 50338344809230
        key = (row_pos, num_pos)
        if key not in self.cache:
            res = 0
            if self._can_use(row_pos, cur_number):
                res += self.solve(row_pos + cur_number + 1, num_pos + 1)
            if self.row[row_pos] in ("?","."):
                res += self.solve(row_pos+1, num_pos)
            self.cache[key] = res

        return self.cache[key]

    def _can_use(self, row_pos, number):
        if row_pos+number >= len(self.row):
            return False
        all_valid = all([self.row[_] in ("?", "#") for _ in range(row_pos, row_pos+number)])
        next_valid = self.row[row_pos+number] in ("?", ".")
        return all_valid and next_valid
def solve_a(data: str):
    data = data.split("\n")

    rows = []
    for row in data:
        springs, numbers = row.split()
        numbers = list(map(int, numbers.split(",")))
        rows.append(Row(springs, numbers))

    res = 0
    for row in rows:
        res += row.solve()
    return res
def solve_b(data: str):
    data = data.split("\n")

    rows = []
    for row in data:
        springs, numbers = row.split()
        numbers = list(map(int, numbers.split(",")))
        rows.append(Row(springs, numbers, True))

    res = 0
    for row in rows:
        print(row.solve())
        res += row.solve()
    return res

def main():
    example: Example
    # A
    examples = [(
"""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""",21)
    ]
    # print("Running task A")
    # for example in examples:
    #     solved = solve_a(example[0])
    #     print("My solution ", solved, "expected", example[1])
    # print(solve_a(puzzle.input_data))

    # # B
    print("Running task B")
    for example in examples:
        solved = solve_b(example[0])
        print("My solution ", solved, "expected", example[1])
    print(solve_b(puzzle.input_data))
    #
if __name__ == '__main__':
    main()