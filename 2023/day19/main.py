import re

from aocd.examples import Example
from aocd.get import current_day, most_recent_year
from aocd.models import default_user, Puzzle
import os
os.environ["AOC_SESSION"] = "53616c7465645f5f2fc428bfbc698864ca265a1cb242f2644a35b22ffb3eacdc9f7e86272333aae8f94366575482a84792fbc84e14cb2aff0ee698822c380e01"
user = default_user()
day = current_day()
year = most_recent_year()
puzzle = Puzzle(year=year, day=day, user=user)
class Instruction:
    def __init__(self, field, value, operator, target, workflow, pos_in_workflow):
        self.field = field
        self.value = value
        self.operator = operator
        self.target = target
        self.workflow = workflow
        self.pos_in_workflow = pos_in_workflow

    def __call__(self, data: dict):
        if self.field is None:
            return self.target
        data_value = data[self.field]
        match self.operator:
            case "<":
                return self.target if data_value < self.value else None
            case ">":
                return self.target if data_value > self.value else None
            case _: return self.target

    def solve_b(self, data: dict):
        if self.field is None:
            return [(self.target, 0, data)]
        res = []
        match self.operator:
            case "<":
                tmp_a = {**data}
                tmp_b = {**data}
                if data[self.field+'_start']<self.value:
                    tmp_a[self.field+"_end"] = min(self.value-1, tmp_a[self.field+"_end"])
                    res.append((self.target,0, tmp_a))
                if data[self.field+"_end"] >= self.value:
                    tmp_b[self.field + "_start"] = max(self.value, tmp_b[self.field+"_start"])
                    res.append((self.workflow, self.pos_in_workflow+1, tmp_b))
            case ">":
                tmp_a = {**data}
                tmp_b = {**data}
                if data[self.field + '_start'] <= self.value:
                    tmp_a[self.field + "_end"] = min(self.value, tmp_a[self.field+"_end"])
                    res.append((self.workflow, self.pos_in_workflow+1, tmp_a))
                if data[self.field + "_end"] > self.value:
                    tmp_b[self.field + "_start"] = max(self.value+1, tmp_b[self.field+"_start"])
                    res.append((self.target, 0, tmp_b))
        return res



class Workflow:
    def __init__(self, instructions):
        self.instructions = instructions

    def __call__(self, data: dict):
        target = None
        for ins in self.instructions:
            target = ins(data)
            if target is not None:
                return target
        return None




def solve_a(data: str):
    workflows, rows = data.split("\n\n")
    created_workflows = {}

    for workflow in workflows.split("\n"):
        matched = re.match(r"(?P<name>.*){(?P<instructions>.*)}", workflow)
        matched = matched.groupdict()
        created_instructions = []
        for instruction in matched["instructions"].split(","):

            matched_instruction = re.match("(?P<field>.*)(?P<operator>[<>])(?P<value>\d+):(?P<target>.*)", instruction)
            if matched_instruction:
                matched_instruction = matched_instruction.groupdict()
                created_instructions.append(Instruction(
                    field=matched_instruction["field"],
                    operator=matched_instruction["operator"],
                    value=int(matched_instruction["value"]),
                    target=matched_instruction["target"],
                    workflow=matched["name"],
                    pos_in_workflow=len(created_instructions)
                ))
            else:
                created_instructions.append(Instruction(None, None, None, instruction))
        created_workflows[matched["name"]] = Workflow(created_instructions)

    res = 0
    for row in rows.split("\n"):
        row = {k:int(v) for k,v in map(lambda x: x.split("="), row.strip()[1:-1].split(","))}
        state = "in"
        while state not in ["R", "A"]:
            state = created_workflows[state](row)

        if state == "A":
            res += sum(row.values())
    return res



def solve_b(data: str):
    workflows, rows = data.split("\n\n")
    created_workflows = {}

    for workflow in workflows.split("\n"):
        matched = re.match(r"(?P<name>.*){(?P<instructions>.*)}", workflow)
        matched = matched.groupdict()
        created_instructions = []
        for instruction in matched["instructions"].split(","):

            matched_instruction = re.match("(?P<field>.*)(?P<operator>[<>])(?P<value>\d+):(?P<target>.*)", instruction)
            if matched_instruction:
                matched_instruction = matched_instruction.groupdict()
                created_instructions.append(Instruction(
                    field=matched_instruction["field"],
                    operator=matched_instruction["operator"],
                    value=int(matched_instruction["value"]),
                    target=matched_instruction["target"],
                    workflow=matched["name"],
                    pos_in_workflow=len(created_instructions)
                ))
            else:
                created_instructions.append(Instruction(None, None, None, instruction, matched["name"], pos_in_workflow=len(created_instructions)))
        created_workflows[matched["name"]] = Workflow(created_instructions)

    stack = [("in",0,{"x_start": 1, "x_end": 4000, "m_start": 1, "m_end":4000, "a_start": 1, "a_end":4000, "s_start": 1, "s_end":4000})]
    com = []
    while len(stack) > 0:
        cur_workflow, cur_instruction, cur_data = stack.pop()
        if cur_workflow == "A":
            com.append(cur_data)
            continue
        if cur_workflow =="R":
            continue



        instruction = created_workflows[cur_workflow].instructions[cur_instruction]
        stack.extend(instruction.solve_b(cur_data))
    print(com)
    res = 0
    for c in com:
        cur = 1
        for ch in ["x", "m", "a", "s"]:
            cur *= (c[ch+"_end"] - c[ch+"_start"]+1)
        res += cur
    return res

def read_examples():
    with open("example.txt") as file:
        content = file.read()

    values = content.split("\n!---!\n")
    return [_ for _ in zip(values[0::2], values[1::2])]


def main():
    # A
    # print("Running task A")
    # for example in read_examples():
    #     solved = solve_a(example[0])
    #     print("My solution ", solved, "expected", example[1])
    # print(solve_a(puzzle.input_data))

    # B
    print("Running task B")
    for example in read_examples():
        solved = solve_b(example[0])
        print("My solution ", solved, "expected", example[1])
    print(solve_b(puzzle.input_data))

if __name__ == '__main__':
    main()