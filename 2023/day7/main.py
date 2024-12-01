from collections import Counter

from aocd.examples import Example
from aocd.get import current_day, most_recent_year
from aocd.models import default_user, Puzzle
import os
os.environ["AOC_SESSION"] = "53616c7465645f5f2fc428bfbc698864ca265a1cb242f2644a35b22ffb3eacdc9f7e86272333aae8f94366575482a84792fbc84e14cb2aff0ee698822c380e01"
user = default_user()
day = current_day()
year = most_recent_year()
puzzle = Puzzle(year=year, day=day, user=user)

class Hand:
    CARD_MAP = {
        **{str(i):i for i in range(1,10)},
        "T":10,
        "J":0,
        "Q":12,
        "K":13,
        "A":14
    }
    def __init__(self, hand: str, bid: str):
        self.hand = hand.strip()
        self.bid = int(bid)
        self.type = self.get_type()

    def get_type(self):
        cn = Counter(self.hand)
        values = tuple(sorted(cn.values(), reverse=True))
        return self._values_to_type(values)

    def _values_to_type(self, values: tuple):
        match values:
            case (5, ): return 6
            case (4,1): return 5
            case (3,2): return 4
            case (3,1,1): return 3
            case (2,2,1): return 2
            case (2,1,1,1): return 1
            case (1,1,1,1,1): return 0
        raise ValueError(f"Got {values}")

    def __lt__(self, other: "Hand"):
        if self.type > other.type:
            return False
        if self.type < other.type:
            return True

        for a,b in zip(self.hand, other.hand):
            if Hand.CARD_MAP[a] > other.CARD_MAP[b]:
                return False
            if Hand.CARD_MAP[a] < other.CARD_MAP[b]:
                return True
        return True


class Hand2(Hand):



    def get_type(self):
        cn = Counter(self.hand)
        values = tuple(sorted(cn.values(), reverse=True))
        j_c = cn["J"]
        if j_c == 0 or j_c == 5:
            return self._values_to_type(values)
        match (values, j_c):
            case ((4,1),_): return self._values_to_type((5,))

            case ((3,2),_): return self._values_to_type((5,))

            case ((3,1,1), _): return self._values_to_type((4,1))

            case ((2,2,1), 1): return self._values_to_type((3,2))
            case ((2,2,1), 2): return self._values_to_type((4,1))

            case ((2,1,1, 1), _): return self._values_to_type((3,1,1))
            case ((1,1,1,1,1), _): return self._values_to_type((2,1,1,1))



        raise ValueError(f"{values}")
#250757288
#250619735
#250731217
#251814355
#251302021
    def __lt__(self, other: "Hand"):
        if self.type > other.type:
            return False
        if self.type < other.type:
            return True

        for a,b in zip(self.hand, other.hand):
            if Hand.CARD_MAP[a] > other.CARD_MAP[b]:
                return False
            if Hand.CARD_MAP[a] < other.CARD_MAP[b]:
                return True
        return True
def solve_a(data: str):
    lines = data.split("\n")
    hands = [Hand(*_.split()) for _ in lines ]
    hands = sorted(hands)
    print([_.hand for _ in hands])
    return sum([(i+1)*h.bid for i,h in enumerate(hands)])

def solve_b(data: str):
    lines = data.split("\n")
    hands = [Hand2(*_.split()) for _ in lines ]
    hands = sorted(hands)
    for hand in hands:
        print(hand.type, hand.hand)
    print([_.hand for _ in hands])
    return sum([(i+1)*h.bid for i,h in enumerate(hands)])


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