from dataclasses import dataclass
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
@dataclass
class Mapping:
    start_to: int
    start_from: int
    range: int

@dataclass
class Range:
    start: int
    length: int

@dataclass
class Layer:
    mappings: List[Mapping]

    def transform(self, val: int):
        for mapping in self.mappings:
            if mapping.start_from <= val < mapping.start_from+mapping.range:
                return val + mapping.start_to - mapping.start_from
        return val

    def transform_ranges(self, ranges: List[Range]):
        stack = ranges
        res = []
        for mapping in self.mappings:
            ns = []
            while stack:
                range = stack.pop()
                # (r.s, r.e,m.s)

                before = (range.start, min(range.start+range.length, mapping.start_from))
                mid = (max(range.start, mapping.start_from), min(range.start+range.length, mapping.start_from+mapping.range))
                after = (min(range.start+range.length, mapping.start_from+mapping.range), range.start+range.length)

                if before[0] < before[1]:
                    ns.append(Range(before[0], before[1]-before[0]))
                if mid[0] < mid[1]:
                    res.append(Range(mid[0]+mapping.start_to-mapping.start_from, mid[1]- mid[0]))
                if after[0] < after[1]:
                    ns.append(Range(after[0], after[1]-after[0]))
            stack = ns
        return res+stack
def solve_a2(data: str):
    seeds, *other = data.split("\n\n")
    seeds = list(map(int, seeds.split(":")[1].split()))

    layers = []
    for layer in other:
        layer = layer.split("\n")[1:]
        cur = []
        for mapping in layer:
            cur.append(Mapping(*map(int, mapping.split())))
        layers.append(Layer(cur))

    results = []
    for seed in seeds:
        for layer in layers:
            seed = layer.transform(seed)

        results.append(seed)
    return min(results)
def solve_b2(data: str):
    seeds, *other = data.split("\n\n")
    seeds = list(map(int, seeds.split(":")[1].split()))

    layers = []
    for layer in other:
        layer = layer.split("\n")[1:]
        cur = []
        for mapping in layer:
            cur.append(Mapping(*map(int, mapping.split())))
        layers.append(Layer(cur))

    seeds = [Range(a,b) for a,b in zip(seeds[::2], seeds[1::2])]
    for layer in layers:
        seeds = layer.transform_ranges(seeds)
    return min([_.start for _ in seeds])

def solve_a(data: str):
    lines = data.split("\n")
    seeds = lines[0]
    seeds = list(map(int, seeds.split(":")[1].split()))
    maps = []
    cur_map = []
    for line in lines[2:]:
        line = line.strip()
        if not line or not line[0].isdigit():
            if len(cur_map) > 0:
                maps.append(cur_map)
                cur_map = []
            continue
        cur_map.append(Mapping(*(map(int, line.split()))))
    if len(cur_map) > 0:
        maps.append(cur_map)

    states = seeds
    for mappings in maps:
        new_states = []
        for state in states:
            new_state = state
            for single_mapping in mappings:
                diff = state - single_mapping.start_b
                if 0 <= diff < single_mapping.range:
                    new_state = single_mapping.start_a+diff
            new_states.append(new_state)
        states = new_states

    return min(states)
def solve_b(data: str):

    lines = data.split("\n")
    seeds = lines[0]
    seeds = list(map(int, seeds.split(":")[1].split()))

    maps = []

    cur_map = []
    for line in lines[2:]:
        line = line.strip()
        if not line or not line[0].isdigit():
            if len(cur_map) > 0:
                maps.append(cur_map)
                cur_map = []
            continue

        cur_map.append(Mapping(*(map(int, line.split()))))
    if len(cur_map) > 0:
        maps.append(cur_map)


    ranges = []
    for start, length in zip(seeds[0::2], seeds[1::2]):
        ranges.append(Range(start, length))
    print(ranges)
    def transform_range(range: Range, mapping: Mapping):
        # Return tuple Transformed ranges and new ranges
        if range.start+range.length <= mapping.start_b:
            return None,[range]
        if range.start >= mapping.start_b+mapping.range:
            return None, [range]

        new_start = max(range.start, mapping.start_b)
        new_end = min(range.start+range.length, mapping.start_b+mapping.range)
        new_range = Range(new_start, new_end-new_start)
        old_ranges = []
        if new_range.start > range.start:
            old_ranges.append(Range(range.start, new_range.start-range.start))
        if new_range.start+new_range.length < range.start+range.length:
            old_ranges.append(Range(new_range.start+new_range.length, (range.start+range.length)-new_start-new_range.length))
        return Range(mapping.start_a-mapping.start_b+new_range.start, new_range.length), old_ranges

    for mappings in maps:
        new_ranges = []
        ranges_for_mapping = []
        for single_mapping in mappings:
            for range in ranges:
                new_range, old_ranges = transform_range(range, single_mapping)
                if new_range:
                    new_ranges.append(new_range)
                if len(old_ranges):
                    ranges_for_mapping.extend(old_ranges)
            ranges = ranges_for_mapping
            ranges_for_mapping = []

        ranges = new_ranges + ranges
    return min([_.start for _ in ranges if _.length > 0])


def main():
    example: Example
    # A
    print("Running task A")
    for example in puzzle.examples:
        # solved = solve_a(example.input_data)
        solved2 = solve_a2(example.input_data)
        print("My solution ", solved2, "expected", example.answer_a)
    print(solve_a2(puzzle.input_data))

    # B
    print("Running task B")
    for example in puzzle.examples:
        solved = solve_b2(example.input_data)
        print("My solution ", solved, "expected", example.answer_b)
    # print(solve_b(puzzle.input_data))
    #
if __name__ == '__main__':
    main()