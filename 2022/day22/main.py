import copy
import functools
import itertools
import multiprocessing
import operator
import re
import struct
from dataclasses import dataclass
from typing import List, Tuple, Dict, Union
import tqdm

@dataclass
class Monkey:
    name: str
    num: int = None
    wait_monkeys: Tuple[str, str] = None
    wait_count: int = 0
    op: str = None
def parse_input(in_lines: List[str]):
    re_number = re.compile("(?P<name>.*): (?P<num>\d+)")
    re_op = re.compile("(?P<name>.*): (?P<first>.+) (?P<op>.) (?P<second>.+)")

    res = []
    for line in in_lines:
        num_r = re_number.match(line)
        if num_r:
            name, num = num_r.groups()
            res.append(Monkey(name, num=int(num)))
        else:
            op_r = re_op.match(line)
            name, first, op, second = op_r.groups()
            res.append(Monkey(name, wait_monkeys=(first, second), wait_count=2, op=op))

    return res


def solve_first(parsed_input, timelimit=24):
    monkeys: List[Monkey] = parsed_input
    queue = [_ for _ in monkeys if _.wait_count == 0]
    monkeys_dict = {_.name:_ for _ in monkeys}

    waits = {}
    for m in monkeys:
        if m.wait_count > 0:
            cur = waits.get(m.wait_monkeys[0], set())
            cur.add(m.name)
            waits[m.wait_monkeys[0]] = cur

            cur = waits.get(m.wait_monkeys[1], set())
            cur.add(m.name)
            waits[m.wait_monkeys[1]] = cur

    queue_poz = 0
    while queue_poz < len(queue):
        cur: Monkey = queue[queue_poz]
        queue_poz += 1

        if cur.num is None:
            a = monkeys_dict[cur.wait_monkeys[0]].num
            b = monkeys_dict[cur.wait_monkeys[1]].num
            match cur.op:
                case "+":
                    cur.num = a + b
                case "-":
                    cur.num = a - b
                case "*":
                    cur.num = a * b
                case "/":
                    cur.num = a / b
                case "=":
                    cur.num = a - b

        if cur.name == "root":
            return cur.num

        waiting: Monkey
        for waiting in waits[cur.name]:
            waiting = monkeys_dict[waiting]
            waiting.wait_count -= 1
            if waiting.wait_count == 0:
                queue.append(waiting)


def solve_second(parsed_input, step=4):
    monkeys: List[Monkey] = parsed_input
    monkeys_dict = {_.name: _ for _ in monkeys}
    monkeys_dict["root"].op = "="

    monkeys_dict["humn"].num = 0
    cur = copy.deepcopy(list(monkeys_dict.values()))
    v1 = solve_first(cur)

    monkeys_dict["humn"].num = 1
    cur = copy.deepcopy(list(monkeys_dict.values()))
    v2 = solve_first(cur)

    v = v1 // (v1-v2)
    monkeys_dict["humn"].num = int(v)
    cur = copy.deepcopy(list(monkeys_dict.values()))
    res = solve_first(cur)
    return int(v)


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
        print("-"*50)