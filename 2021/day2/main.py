import itertools
import operator
from typing import List

def solve(lines: List[str]):
    h,v = 0,0
    aim = 0
    lines = [str.strip(_) for _ in lines]
    for line in lines:
        match line.split(" "):
            case "forward", x:
                h += int(x)
                v += int(x)*aim
            case "back", x:
                h -= int(x)
            case "up", x:
                aim -= int(x)
            case "down", x:
                aim += int(x)
        # print(h,v,aim)
    return abs(h * v)


if __name__ == '__main__':
    with open("input1.txt") as file:
        lines = file.readlines()
    print("Example res", solve(lines))

    print("Test data")
    with open("input2.txt") as file:
        lines = file.readlines()
    print("Test res", solve(lines))