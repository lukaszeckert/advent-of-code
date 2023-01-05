import re
from dataclasses import dataclass
from typing import List


@dataclass
class Monkey:
    items: List[int]
    op_val: str
    op: str
    div: int
    true_id: int
    false_id: int
    inspections = 0

    def get_op_val(self, item):
        if self.op_val.strip() == "old":
            return item
        return int(self.op_val)



with open("input2.txt") as file:
    lines = file.readlines()
lines = [_.strip() for _ in lines]

"""
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3
"""
monkey_re = re.compile(
r"""Monkey \d+:
Starting items: (.*)
Operation: new = old (.) (.+)
Test: divisible by (\d+)
If true: throw to monkey (\d+)
If false: throw to monkey (\d+)""", re.MULTILINE
)
print(monkey_re.match(
"""Monkey 0:
Starting items: 79, 98
Operation: new = old * 19
Test: divisible by 23
If true: throw to monkey 2
If false: throw to monkey 3""").groups())

re_items = re.compile("Starting items: (.*)")
re_operation = re.compile("Operation: new = old (?P<operation>.) (?P<value>.*)")
re_test = re.compile("Test: divisible by (\d+)")
re_test_true = re.compile("If true: throw to monkey (\d+)")
re_test_false = re.compile("If false: throw to monkey (\d+)")


monkeys = []
i = 0
while i < len(lines):
    cur_lines = '\n'.join(lines[i:i + 6])
    re_res = monkey_re.match(cur_lines)

    items = [int(_.strip()) for _ in re_res.groups()[0].split(",")]
    operation = re_res.groups()[1]
    op_val = re_res.groups()[2]
    test_val = int(re_res.groups()[3])
    test_val_true = int(re_res.groups()[4])
    test_val_false = int(re_res.groups()[5])

    monkeys.append(Monkey(
        items, op_val, operation, test_val, test_val_true, test_val_false
    ))

    i += 7

all_div = set([_.div for _ in monkeys])
for m in monkeys:
    items = []
    for i in m.items:
        item = {}
        for d in all_div:
            item[d] = i % d
        items.append(item)
    m.items = items


for j in range(10000):
    for m in monkeys:
        for i,item in enumerate(m.items):
            m.inspections += 1

            n_item = {}
            for d in all_div:
                if m.op == "*":
                    op_v = m.get_op_val(item[d])
                    n_v = item[d]*op_v
                elif m.op == "+":
                    op_v = m.get_op_val(item[d])
                    n_v = item[d]+op_v
                n_item[d] = n_v % d

            if n_item[m.div] == 0:
                monkeys[m.true_id].items.append(n_item)
            else:
                monkeys[m.false_id].items.append(n_item)

        m.items = []
    if j in [0, 19, 999, 1999, 2999, 3999,4999,5999,6999,7999,8999,9999]:
        print([_.inspections for _ in monkeys])


print([_.inspections for _ in monkeys])
sol1 = sorted([_.inspections for _ in monkeys])[-2:]
sol1 = sol1[0]*sol1[1]
print(sol1)
