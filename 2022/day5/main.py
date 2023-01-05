from dataclasses import dataclass


@dataclass
class Command:
    num: int
    from_stack: int
    to_stack: int

def parse_current_stacks(lines):
    stacks = []

    for line in lines:
        line = line.rstrip()
        for s in range(10):
            pos = s*4+1
            if pos < len(line):
                if line[pos] != ' ':
                    while len(stacks) <= s:
                        stacks.append([])
                    stacks[s].append(line[pos])

    return stacks

def parse_commands(lines):
    commands = []
    for line in lines:
        line = line.strip().split(" ")

        num = int(line[1])
        from_stack = int(line[3])
        to_stack = int(line[5])
        commands.append(Command(
            num, from_stack, to_stack
        ))
    print(commands)

    return commands


def parse_file(lines):
    for i, line in enumerate(lines):
        if line == "\n":
            break
    break_point = i
    stacks = parse_current_stacks(lines[:break_point-1])
    commands = parse_commands(lines[break_point+1:])
    return stacks, commands

with open("input2.txt") as file:
    lines = file.readlines()

stacks, commands = parse_file(lines)

for i in range(len(stacks)):
    stacks[i] = stacks[i][::-1]

for command in commands:
    values = []
    for _ in range(command.num):
        values.append(stacks[command.from_stack-1].pop())

    stacks[command.to_stack-1].extend(values[::-1])

for s in stacks:
    print(s[-1], end="")
