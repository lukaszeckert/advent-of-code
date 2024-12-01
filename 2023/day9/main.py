from aocd.examples import Example
from aocd.get import current_day, most_recent_year
from aocd.models import default_user, Puzzle
import os

os.environ[
    "AOC_SESSION"] = "53616c7465645f5f2fc428bfbc698864ca265a1cb242f2644a35b22ffb3eacdc9f7e86272333aae8f94366575482a84792fbc84e14cb2aff0ee698822c380e01"
user = default_user()
day = current_day()
year = most_recent_year()
puzzle = Puzzle(year=year, day=day, user=user)


class Power:
    def __init__(self, first_layer):
        self.layers = [first_layer]
        self.reversed = False

    def solve(self):
        while len(set(self.layers[-1])) != 1:
            new_layers = [cur - prev for prev, cur in zip(self.layers[-1], self.layers[-1][1:])]
            self.layers.append(new_layers)

    def gen_next(self):
        for i, layer in reversed(list(enumerate(self.layers))):
            if i == len(self.layers) - 1:
                layer.append(layer[-1])
            else:
                if self.reversed:
                    layer.append(-self.layers[i + 1][-1] + layer[-1])
                else:
                    layer.append(self.layers[i + 1][-1] + layer[-1])
        return self.layers[0][-1]

    def reverse(self):
        self.layers = [_[::-1] for _ in self.layers]
        self.reversed = True


def solve_a(data: str):
    exp = [list(map(int, _.split())) for _ in data.split("\n")]
    powers = [Power(_) for _ in exp]
    for p in powers: p.solve()
    res = [p.gen_next() for p in powers]
    print(res)
    return sum(res)


def solve_b(data: str):
    exp = [list(map(int, _.split())) for _ in data.split("\n")]
    powers = [Power(_) for _ in exp]
    for p in powers:
        p.solve()
        p.reverse()
    res = [p.gen_next() for p in powers]
    print(res)
    return sum(res)


def main():
    example: Example
    # A
    # print("Running task A")
    # for example in puzzle.examples:
    #     solved = solve_a(example.input_data)
    #     print("My solution ", solved, "expected", example.answer_a)
    # print(solve_a(puzzle.input_data))

    # B
    print("Running task B")
    for example in puzzle.examples:
        solved = solve_b(example.input_data)
        print("My solution ", solved, "expected", example.answer_b)
    print(solve_b(puzzle.input_data))


if __name__ == '__main__':
    main()
