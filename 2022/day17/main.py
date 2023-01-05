import functools
import itertools
import operator
import re
import struct
from dataclasses import dataclass
from typing import List, Tuple, Dict
import tqdm

def parse_input(in_lines: List[str]):
    rocks = [[(2,0),(3,0), (4,0), (5,0)],
             [(3,2), (2,1), (3,1), (4,1), (3,0)],
             [(2,0),(3,0), (4,0), (4,1), (4,2)],
             [(2,0), (2,1), (2,2),(2,3)],
             [(2,1), (3,1), (2,0), (3,0)]
             ]



    return in_lines[0].strip(),rocks

def vis(oc):
    window = 100
    m = max([_[1] for _ in oc])
    res = [["." for _ in range(7)] for _ in range(window+1)]
    for x,y in oc:
        if y >= m-window:
            res[m-y][x] = "#"

    return '\n'.join([''.join(_) for _ in res])
    for row in reversed(res[-5:]):
        print(''.join(row))

def solve_first(parsed_input, num):
    flow, rocks = parsed_input

    oc = set([(_, 0) for _ in range(7)])
    res = 0
    r = 0
    f = 0
    prev = 0
    seen = dict()
    # z = 1000000000000
    # z1 = z
    # zm = z1//len(flow)
    # rm = z1-zm*len(flow)
    # # next_stop = -1
    # #
    # print(zm, rm, len(flow))
    # # rr = 47878
    # print(zm*79774+5175)
    # print(rm)
    print(10*len(flow))
    for r in tqdm.tqdm(range(num)):
        oc = set((x,y) for x,y in oc if res-200<=y or y == 0)

        v = vis(oc)
        v = (v,f%(len(flow)))

        if v in seen:
            print("HIT", r, f%len(flow), seen[v])
        if f > 1000:
            seen[v] = res
        # if r == 3254:
        #     print(res, 'a')
        #
        # if (r) % (len(flow)*len(rocks)) == 0:
        #
        #     v = vis(oc)
        #     # print(v)
        #     if v in seen:
        #         print(oc)
        #         print(r, seen[v], res-seen[v][1], "Hit")
        #     seen[v] = (r,res)

            # print(res-prev)
            # prev = res
        cur_r = rocks[r%len(rocks)]
        # r += 1

        cur_r = [(x,y+res+4) for x,y in cur_r]
        while True:
            # jet

            is_left = flow[f%len(flow)] == "<"
            f += 1
            dx = 1
            if is_left:
                dx = -1

            n_cur = [(x+dx, y) for x,y in cur_r]
            if 0 <= min([_[0] for _ in n_cur]) <= max([_[0] for _ in n_cur]) < 7:
                if not any([_ in oc for _ in n_cur]):
                  cur_r = n_cur



            # down
            n_cur = [(x, y-1) for x,y in cur_r]
            if any([_ in oc for _ in n_cur]):
                for _ in cur_r:
                    res = max(res, _[1])
                    oc.add(_)
                break
            cur_r = n_cur

    return res

def solve_second(parsed_input):
    solve_first(parsed_input, 10000000000)
    for _ in range(100):
        print(_, solve_first(parsed_input, len(parsed_input[0])*(_+1))-solve_first(parsed_input, len(parsed_input[0])*_))


if __name__ == '__main__':
    for solver in (
            # solve_first,
            solve_second,
    ):
        with open("input1.txt") as file:
            lines = file.readlines()

        # print("Example res", solver(parse_input(lines)))

        print("Test data")
        with open("input2.txt") as file:
            lines = file.readlines()
        print("Test res", solver(parse_input(lines)))
