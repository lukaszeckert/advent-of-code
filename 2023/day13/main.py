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

def find_sym(rows):
    res = [0]
    for i in range(1,len(rows)):
        up = rows[:i]
        down = rows[i:]
        total_len = min(len(up), len(down))
        up = up[-total_len:]
        down = down[:total_len]
        if up == down[::-1]:
            res.append(i)
    return res

def solve_single_a(data: str):
    rows = data.split("\n")
    reflection_lines = {"r": find_sym(rows)}
    res = 100*sum(find_sym(rows))
    t_rows = [_ for _ in rows[0]]
    for row in rows[1:]:
        for i,ch in enumerate(row):
            t_rows[i] += ch

    reflection_lines["c"] = find_sym(t_rows)
    res += sum(find_sym(t_rows))
    return res, reflection_lines


def solve_a(data: str):
    problems = data.split("\n\n")
    res = 0
    for p in problems:
        tmp, _ = solve_single_a(p)
        res += tmp
    return res

def solve_b(data: str):

    problems = data.split("\n\n")
    res = 0
    rev = {".":"#", "#":"."}


    for p in tqdm.tqdm(problems):
        _, org_lines = solve_single_a(p)
        rows = p.split("\n")
        for i,_ in enumerate(rows):
            for j,_ in enumerate(rows[i]):
                tmp = list(rows[i])
                tmp[j] = rev[tmp[j]]
                rows[i] = ''.join(tmp)
                _, lines = solve_single_a('\n'.join(rows))
                new_row = set(lines["r"]).difference(org_lines["r"])
                new_column =set(lines["c"]).difference(org_lines["c"])
                res += sum(new_row)*100+sum(new_column)
                tmp[j] = rev[tmp[j]]
                rows[i] = ''.join(tmp)
    return res//2

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