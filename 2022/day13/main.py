import json
import logging
import operator

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

with open("input1.txt") as file:
    lines = file.readlines()


def is_right(left, right):
    match (left, right):
        case (int(), int()):
            return right-left
        case (list(), list()):
            cur = next(filter(lambda x: x != 0, map(
                lambda _: is_right(*_), zip(left, right))), 0)
            if not cur:
                cur = len(right)-len(left)
            return cur
        case (int(), _):
            return is_right([left], right)
        case (_, int()):
            return is_right(left, [right])


lines = filter(lambda x: x, map(str.strip, lines))
signals = list(map(json.loads, lines))
pairs = list(zip(signals[::2], signals[1::2]))

res1 = sum([i + 1 if is_right(*_) > 0 else 0 for i, _ in enumerate(pairs)])
first, second = [sum([1 if is_right(_, sep) > 0 else 0 for _ in signals]) for sep in ([[2]], [[6]])]
print(res1, (first + 1) * (second + 2))

logger.info(f"test1")
logger.debug(f"test2")
print("A")