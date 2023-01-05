import functools
import itertools
import operator
import re
import struct
from dataclasses import dataclass
from typing import List, Tuple, Dict
import tqdm


@dataclass
class Node:
    id: str
    flow: int
    edges: List[str]
    dist: Dict[str, int] = None

def parse_input(in_lines: List[str]):
    re_sb = re.compile("Valve (.*) has flow rate=(-?\d+); tunnels? leads? to valves? (.*)")
    nodes = {}

    for line in in_lines:
        (valve, flow, edges) = re_sb.findall(line)[0]
        nodes[valve] = Node(valve, int(flow), [_.strip() for _ in edges.split(",")])

    starts = [_ for _ in nodes if nodes[_].flow > 0]+["AA"]
    for s in starts:
        dis = {s: 0}
        q = [s]
        poz = 0
        while poz < len(q):
            cur = q[poz]
            poz += 1
            for e in nodes[cur].edges:
                if e not in dis:
                    q.append(e)
                    dis[e] = dis[cur]+1
        del dis[s]
        if "AA" in dis:
            del dis["AA"]
        nodes[s].dist = {k:v for k,v in dis.items() if k in starts}

    aa = nodes["AA"]
    nodes = {k:v for k,v in nodes.items() if v.flow > 0 and k != "AA"}
    return nodes,aa


def solve_first(parsed_input):
    nodes,aa = parsed_input

    def get_score(valves, nodes):
        return sum(nodes[_].flow for _ in valves)


    def brut(cur,el, valves_released: set, renaming_time):
        score = get_score(valves_released, nodes)

        if len(valves_released) == len(nodes):
            return score*renaming_time

        if renaming_time <= 0:
            return 0

        r1 = r2 = 0

        for e, d in nodes[cur].dist.items():
            if e not in valves_released:
                r1 = brut(e, set(valves_released) | {cur}, renaming_time - d - 1)
                r1 += score * min(d + 1, renaming_time)
                r1 += nodes[cur].flow * min(d, renaming_time - 1)
                r2 = max(r2, r1)
        return max(r1,r2, score*renaming_time+nodes[cur].flow*(renaming_time-1))

    res = 0
    # nodes["TT"] = Node("TT",1000, [], {})
    # nodes["BB"].dist["TT"] = 20
    for e, d in aa.dist.items():
        res = max(res, brut(e, set(), 30-d))
    return res


@dataclass(eq=True, unsafe_hash=True)
class Action:
    dest: str
    duration: int
    action: str # "GO" or "OPEN"

def solve_second(parsed_input):
    nodes, aa = parsed_input

    def get_score(valves, nodes):
        return sum(nodes[_].flow for _ in valves)

    all_score = get_score([_ for _ in nodes], nodes)


    best_score = 0
    best_score_hit = 0
    def brut(pa:Action, ea:Action, valves_released: set, renaming_time, prev_score):
        nonlocal best_score
        nonlocal best_score_hit
        score = get_score(valves_released, nodes)
        if len(valves_released) == len(nodes):
            return score * renaming_time+prev_score

        if prev_score + all_score*renaming_time < best_score:
            best_score_hit += 1
            if best_score_hit % 100000 == 0:
                print(best_score, best_score_hit, prev_score+all_score*renaming_time, len(valves_released))
            return -1
        if renaming_time <= 0:
            return prev_score

        wait = min(pa.duration, ea.duration)
        if wait > 0:
            wait = min(wait, renaming_time)
            return brut(Action(pa.dest, pa.duration-wait, pa.action), Action(ea.dest, ea.duration-wait, ea.action), valves_released, renaming_time-wait, prev_score+score*wait)

        next_pa = []
        if pa.duration == 0:
            if pa.action == "OPEN":
                valves_released = tuple(set(valves_released) | {pa.dest})
            if pa.dest not in valves_released:
                next_pa.append(Action(pa.dest, 1, "OPEN"))
            else:
                for e, d in nodes[pa.dest].dist.items():
                    if e not in valves_released:
                        next_pa.append(Action(e, d, "GO"))

        else:
            next_pa.append(pa)
        if len(next_pa) == 0:
            next_pa.append(Action(pa.dest, 1000, "GO"))

        next_ea = []
        if ea.duration == 0:
            if ea.action == "OPEN":
                valves_released = tuple(set(valves_released) | {ea.dest})
            if ea.dest not in valves_released:
                next_ea.append(Action(ea.dest, 1, "OPEN"))
            else:
                for e, d in nodes[ea.dest].dist.items():
                    if e not in valves_released:
                        next_ea.append(Action(e, d, "GO"))
        else:
            next_ea.append(ea)
        if len(next_ea) == 0:
            next_ea.append(Action(ea.dest, 1000, "GO"))

        res = 0
        for c,e in itertools.product(next_pa, next_ea):
                if not (c == e and len(valves_released)+1 < len(nodes)):
                    res = max(res, brut(c, e, valves_released, renaming_time, prev_score))
                    best_score = max(res, best_score)

        return res


    # print(nodes)
    # for e,d in aa.dist.items():
    #     print(e, d, nodes[e].flow)
    # return 1

    res = brut(Action("VP", aa.dist["VP"], "GO"), Action("XQ", aa.dist["XQ"], "GO"),(),26, prev_score=0)
    print('A', res)
    res = max(res, brut(Action("VP", aa.dist["VP"], "GO"), Action("VM", aa.dist["VM"], "GO"),(),26, prev_score=0))
    print('V', res)
    for e, d in tqdm.tqdm(aa.dist.items()):
        for el, dl in tqdm.tqdm(aa.dist.items()):
            if el < e:
                res = max(res, brut(Action(e,d, "GO"),Action(el, dl, "GO"), tuple(), 26, 0))
    return res


if __name__ == '__main__':
    for solver in (
              #   solve_first,
            solve_second,
    ):
        with open("input1.txt") as file:
            lines = file.readlines()

        # print("Example res", solver(parse_input(lines)))

        print("Test data")
        with open("input2.txt") as file:
            lines = file.readlines()
        print("Test res", solver(parse_input(lines)))
