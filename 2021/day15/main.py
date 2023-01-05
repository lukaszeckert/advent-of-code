import itertools
import operator
import struct
from dataclasses import dataclass
from queue import PriorityQueue
from typing import List

def parse_input(in_lines: List[str]):
    in_lines = [[int(_) for _ in _.strip()] for _ in in_lines]
    return in_lines

def solve_first(parsed_input:List[List[int]]):
    queue = PriorityQueue()
    distances = {}
    queue.put((0,(0,0)))
    n = len(parsed_input)
    while queue.qsize():
        dis, (x,y) = queue.get()
        for dx,dy in ((1,0), (-1,0), (0,1), (0,-1)):
            nx = x+dx
            ny = y+dy
            if 0 <= nx < n and 0 <= ny < n:
                ndis = dis + parsed_input[nx][ny]
                if distances.get((nx,ny), float("inf")) > ndis:
                    queue.put((dis+parsed_input[nx][ny], (nx, ny)))
                    distances[(nx,ny)] = ndis

    return distances[(n-1,n-1)]


def solve_second(parsed_input):
    new_input = []

    for j in range(5):
        for line in parsed_input:

            row = line[::]
            for i in range(4):
                row.extend([(_+i)%9+1 for _ in line])
            new_input.append(row)
        parsed_input = [[(_)%9+1 for _ in row] for row in parsed_input]

    return solve_first(new_input)



if __name__ == '__main__':
    for solver in (
         solve_first,
         solve_second,
    ):
        with open("input1.txt") as file:
            lines = file.readlines()

        print("Example res", solver(parse_input(lines)))

        print("Test data")
        with open("input2.txt") as file:
            lines = file.readlines()
        print("Test res", solver(parse_input(lines)))


