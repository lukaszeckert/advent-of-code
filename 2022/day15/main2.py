import itertools
import operator
import re
import struct
from dataclasses import dataclass
from typing import List, Tuple
import tqdm


def parse_input(in_lines: List[str]):
    in_lines = [_.strip() for _ in in_lines]
    re_sb = re.compile("(-?\d+)")
    sensors = []
    beacons = []

    for line in in_lines:
        sx, sy, bx, by = map(int, re_sb.findall(line))
        dis = abs(sx - bx) + abs(sy - by)
        sensors.append((dis, (sx, sy)))
        beacons.append((bx, by))

    return sensors, beacons


def solve_first(parsed_input: Tuple[List, List], search_y):
    sensors, beacons = parsed_input
    beacons = set(beacons)
    seen = 0
    m_dis = max([_[0] for _ in sensors])
    min_x = min([_[1][0] for _ in sensors])
    max_x = max([_[1][0] for _ in sensors])

    res = 0
    for pos in range(min_x - m_dis - 1, max_x + m_dis + 2):
        pos = (pos, search_y)
        for dis, (x, y) in sensors:
            if abs(x - pos[0]) + abs(y - pos[1]) <= dis:
                res += 1
                break
    res -= len([_ for _ in beacons if _[1] == search_y])
    return res


def find_sensors(pos, sensors):
    res = set()
    for i, (dis1, (ssx, ssy)) in enumerate(sensors):
        if abs(pos[0] - ssx) + abs(pos[1] - ssy) <= dis1:
            res.add(i)
    return res


def gen_all_points_outside(pos, dist, sensors):
    cur = (pos[0], pos[1] + dist + 1)
    while cur[0] < pos[0] + dist + 1:
        yield cur
        cur = (cur[0] + 1, cur[1] - 1)

    cur = (pos[0], pos[1] + dist + 1)
    while cur[0] > pos[0] - dist - 1:
        yield cur
        cur = (cur[0] - 1, cur[1] - 1)

    cur = (pos[0], pos[1] - dist - 1)
    while cur[0] <= pos[0] + dist + 1:
        yield cur
        cur = (cur[0] + 1, cur[1] + 1)


    cur = (pos[0], pos[1] - dist - 1)
    while cur[0] >= pos[0] - dist - 1:
        yield cur
        cur = (cur[0] - 1, cur[1] + 1)



def solve_second(parsed_input, max_value):
    sensors, _ = parsed_input
    sensors_h = [(_[0], (_[1][0] + _[1][0], _[1][0]-_[1][1])) for _ in sensors]
    y = -max_value
    while y <= max_value:
        available = [_ for _ in sensors_h if abs(_[1][1]-y) <= _[0]]
        next_y = min([_[1][1]+_[0] for _ in available])
        broken = False
        end = None
        d = sorted(available, key=lambda x:x[1][0]-x[0])
        for dis, (x,_) in d:
            if end is None:
                end = x+dis
            if x-dis > end:
                print(x-dis, end)
                broken = True
                break

            end = max(end, x+dis)

        if broken:
            print('a', y, next_y, end)
            # x+y
            # x-y
            x,y = (y+end+1)//2, (end+1-y)//2
            if 0 <= x <= max_value and 0 <= y <= max_value:
                if len(find_sensors((x, y), sensors)) == 0:
                    print(x, y)
                    return x * 4000000 + y

            # for x in tqdm.tqdm(range(max_value+1)):
            #     ny = x-y
            #
            #     # 3405562-3246513
            #     if 0 <= ny <= max_value:
            #         if len(find_sensors((x, ny), sensors)) == 0:
            #             print(x, ny)
            #             return x * 4000000 + ny

        y = next_y+1



if __name__ == '__main__':
    for solver in (
            #     solve_first,
            solve_second,
    ):
        with open("input1.txt") as file:
            lines = file.readlines()

        print("Example res", solver(parse_input(lines), 20))

        print("Test data")
        with open("input2.txt") as file:
            lines = file.readlines()
        print("Test res", solver(parse_input(lines), 4000000))
