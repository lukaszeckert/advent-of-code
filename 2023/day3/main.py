import re
from functools import reduce

import aocd
from aocd.models import Puzzle

with open("full.txt") as file:

    lines = file.readlines()

number_ids ={}
cur_id = 0
lines_with_ids = []
lines = ["."*len(lines[0]), *lines, "."*len(lines[0])]
for line in lines:
    line = "."+line+"."
    cur_line = list(line.strip())

    for number in re.finditer("(\d+)", line):
        # print(line, number, number.span(), number.groups()[0])
        for a in range(*number.span()):
            cur_line[a] = cur_id
            number_ids[cur_id] = int(number.groups()[0])
        cur_id += 1
    lines_with_ids.append(cur_line)

ids_with_symbol = set()
symbols = ['$', '@', '-', '%', '+', '#', '=', '*', '/', '&']
directions = [
    (0,1),
    (0,-1),
    (1,0),
    (-1,0),
    (1,1),
    (1,-1),
    (-1,1),
    (-1,-1)
]
for i,line in enumerate(lines_with_ids):
    for j, element in enumerate(line):
        if isinstance(element, int):
            if any(
                [str(lines_with_ids[i+di][j+dj]) in symbols for di,dj in directions]):
                ids_with_symbol.add(element)

print(sum([number_ids[_] for _ in ids_with_symbol]))

res = 0
for i,line in enumerate(lines_with_ids):
    for j, element in enumerate(line):
        if element == "*":
            numbers = set([lines_with_ids[i+di][j+dj] for di,dj in directions if isinstance(lines_with_ids[i+di][j+dj], int)])
            for a in numbers:
                for b in numbers:
                    if a != b and a<b:
                        print(number_ids[a], number_ids[b])
                        res += number_ids[a]*number_ids[b]

print(res)