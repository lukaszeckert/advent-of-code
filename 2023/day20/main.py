from collections import deque
from typing import List, Tuple

from aocd.examples import Example
from aocd.get import current_day, most_recent_year
from aocd.models import default_user, Puzzle
import os
os.environ["AOC_SESSION"] = "53616c7465645f5f2fc428bfbc698864ca265a1cb242f2644a35b22ffb3eacdc9f7e86272333aae8f94366575482a84792fbc84e14cb2aff0ee698822c380e01"
user = default_user()
day = current_day()
year = most_recent_year()
puzzle = Puzzle(year=year, day=day, user=user)
class Node:
    def __init__(self, name, inputs, outputs):
        self.outputs = outputs
        self.inputs = inputs
        self.name = name

class Conj(Node):

    def __init__(self, name, inputs, outputs):
        super().__init__(name, inputs, outputs)
        self._inputs_states = {_:0 for _ in inputs}
        self._state = None

    def receive(self, receiver, level: int) -> List[Tuple[str, str, int]]:
        self._inputs_states[receiver] = level
        new_state = 1-all(self._inputs_states.values())
        self._state = new_state
        return [(self.name, _, new_state) for _ in self.outputs]
        return []

class Flop(Node):
    def __init__(self, name, inputs, outputs):
        super().__init__(name, inputs, outputs)
        self._state = 0

    def receive(self, receiver, level: int) -> List[Tuple[int ,str]]:
        if level == 0:
            self._state = 1-self._state
            return [(self.name, _,self._state) for _ in self.outputs]
        return []

def parse_input(data: str):
    in_edges = {}
    out_edges = {}
    node_types = {}

    for line in data.split("\n"):
        node, edges = line.split("->")
        node = node.strip()
        edges = [_.strip() for _ in edges.strip().split(',')]

        out_edges[node[1:]] = edges
        node_types[node[1:]] = node[0]

    for k, edges in out_edges.items():
        for edge in edges:
            in_edges[edge] = in_edges.get(edge, []) + [k]

    nodes = {}
    for node_name, node_type in node_types.items():
        match node_type:
            case "%":
                nodes[node_name] = Flop(node_name, in_edges[node_name], out_edges[node_name])
            case "&":
                nodes[node_name] = Conj(node_name, in_edges[node_name], out_edges[node_name])
    return nodes, out_edges["roadcaster"]


def solve_a_iteration(nodes, broadcast):
    queue = deque(
        [("button", _, 0) for _ in broadcast]
    )
    num_high = 0
    num_low = 0
    when = False
    while queue:
        sender, receiver, pulse = queue.popleft()
        # print(sender, "--hight--" if pulse else "--low--", "->", receiver)
        if pulse == 0:
            num_low += 1
        else:
            num_high += 1
        node = nodes.get(receiver)

        if receiver == "lg" and pulse == 1:
            when = True

        if node:
            pulses = node.receive(sender, pulse)
            for p in pulses:
                queue.append(p)
    return num_high, num_low+1, when
def solve_a(data: str):
    nodes, broadcast = parse_input(data)
    num_high, num_low = 0,0
    for _ in range(1000):
        nh, nl,_ = solve_a_iteration(nodes, broadcast)
        num_high += nh
        num_low += nl
    print(num_high, num_low)
    return num_high*num_low
def solve_b(data: str):
    nodes, broadcast = parse_input(data)
    num_high, num_low = 0,0

    observed_nodes = []
    for node in nodes.values():
        if "rx" in node.outputs:
            observed_nodes.append(node.name)
    observed_nodes = nodes["lg"].inputs
    print(observed_nodes, broadcast)
    for br in broadcast:
        for i in range(8000):
            _,_,when = solve_a_iteration(nodes, [br])
            # print(i, br, [nodes[_]._state for _ in observed_nodes])
            if when:
                print(i+1, br)
            # if not any([nodes[_]._state for _ in observed_nodes]):
            #     print(i, br, [nodes[_]._state for _ in observed_nodes])
    #     num_high += nh
    #     num_low += nl
    # print(num_high, num_low)
    return num_high*num_low

def read_examples():
    with open("example.txt") as file:
        content = file.read()

    values = content.split("\n!---!\n")
    return [_ for _ in zip(values[0::2], values[1::2])]


def main():
    # A
    # print("Running task A")
    for example in read_examples():
        solved = solve_a(example[0])
        print("My solution ", solved, "expected", example[1])
    print(solve_a(puzzle.input_data))
    #
    # # B
    print("Running task B")
    # for example in read_examples():
    #     solved = solve_b(example[0])
    #     print("My solution ", solved, "expected", example[1])
    print(solve_b(puzzle.input_data))
    #
if __name__ == '__main__':
    main()