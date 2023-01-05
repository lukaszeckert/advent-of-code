import functools
import itertools
import multiprocessing
import operator
import re
import struct
from dataclasses import dataclass
from typing import List, Tuple, Dict
import tqdm


@dataclass
class Blueprint:
    ore: Dict[str, int]
    clay: Dict[str, int]
    obsidian: Dict[str, int]
    geo: Dict[str, int]

def parse_input(in_lines: List[str]):
    costs_re = re.compile("(\d+)")
    costs = [tuple(map(int, costs_re.findall(_))) for _ in in_lines]

    res = []
    for line in costs:
        line = line[1:]
        res.append(Blueprint(ore={"ore": line[0]}, clay={"ore": line[1]}, obsidian={"ore": line[2], "clay": line[3]},
                             geo={"ore": line[4], "obsidian": line[5]}))
    return res


def _prepare_step(cur_robots, cur_storage, which, cost):
    n_robots = cur_robots.copy()
    if which:
        n_robots[which] += 1

    n_storage = cur_storage.copy()
    for k, v in cur_robots.items():
        n_storage[k] += v
    if cost:
        for k, v in cost.items():
            n_storage[k] -= v

    c = n_storage["geo"]
    n_storage["geo"] = 0
    return n_robots, n_storage, c


def _solve(cur_robots: Dict[str, int], cur_storage: Dict[str, int], remaining_time: int,
           cache: Dict[Tuple, int], best_geo_per_time: Dict[int, int], blueprint: Blueprint):
    _solve_partial = functools.partial(_solve, cache=cache, best_geo_per_time=best_geo_per_time, blueprint=blueprint)

    if remaining_time == 0:
        return 0

    key = tuple(cur_robots.items()) + tuple([(k, min(v,50)) for k, v in cur_storage.items() if k != "geo"]) + (remaining_time,)
    if key not in cache:
        if best_geo_per_time.get(remaining_time, 0) > cur_robots["geo"] + 1:
            return 0
        best_geo_per_time[remaining_time] = max(best_geo_per_time.get(remaining_time, 0), cur_robots["geo"])

        r = 0
        can_buy_ore = all([cur_storage[k] >= v for k, v in blueprint.ore.items()])
        can_buy_clay = all([cur_storage[k] >= v for k, v in blueprint.clay.items()])
        can_buy_obsidian = all([cur_storage[k] >= v for k, v in blueprint.obsidian.items()])
        can_buy_geo = all([cur_storage[k] >= v for k, v in blueprint.geo.items()])

        can_buy_everything = all([
            can_buy_ore, can_buy_clay, can_buy_obsidian, can_buy_geo
        ])
        for cond, name, cost in [
            (can_buy_geo, "geo", blueprint.geo),
            (can_buy_obsidian, "obsidian", blueprint.obsidian),
            (can_buy_clay, "clay", blueprint.clay),
            (can_buy_ore, "ore", blueprint.ore),
            (not can_buy_everything, None, None),

        ]:
            if cond:
                n_robots, n_storage, c = _prepare_step(cur_robots, cur_storage, name, cost)
                r = max(r, _solve_partial(n_robots, n_storage, remaining_time - 1) + c)

        cache[key] = r

    return cache[key]


def solve_first(parsed_input, timelimit=24):
    final = 0
    cur_robots = {"ore": 1, "clay": 0, "obsidian": 0, "geo": 0}
    cur_storage = {"ore": 0, "clay": 0, "obsidian": 0, "geo": 0}

    with multiprocessing.Pool(8) as pool:
        results = pool.starmap(_solve, [(cur_robots, cur_storage, timelimit, dict(), dict(), _) for _ in parsed_input])

    for i, best in enumerate(results):
        print(i, best)
        final += (i + 1) * best
    return final


def solve_second(parsed_input, timelimit=32):
    final = 1
    cur_robots = {"ore": 1, "clay": 0, "obsidian": 0, "geo": 0}
    cur_storage = {"ore": 0, "clay": 0, "obsidian": 0, "geo": 0}

    with multiprocessing.Pool(8) as pool:
        results = pool.starmap(_solve,
                               [(cur_robots, cur_storage, timelimit, dict(), dict(), _) for _ in parsed_input[:3]])

    for i, best in enumerate(results):
        print(i, best)
        final *= best

    return final


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
