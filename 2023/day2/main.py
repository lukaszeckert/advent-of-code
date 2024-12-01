import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Game:
    id: int
    sub_games: List[Dict]
with open("data.in" ) as file:
    lines = file.readlines()

def parse_line(line):
    game_id, sub_games = line.split(":")
    game_id = int(game_id.split(" ")[-1])
    res = []
    for sub_game in sub_games.split(";"):
        cur = {}
        for color in ["red", "green", "blue"]:
            cur[color] = [int(_.groups()[0]) for _ in re.finditer(f"(\d+) {color}", sub_game)]
            if len(cur[color]) > 1:
                print("Failed", line)
                assert False
            if len(cur[color]) == 1:
                cur[color] = cur[color][-1]
            else:
                cur[color] = 0
        res.append(cur)

    a = Game(game_id, res)
    print(line)
    print(a)
    return a


games: List[Game] = [parse_line(_) for _ in lines]
thresholds = {"red": 12, "green": 13, "blue":14}
res = 0
for game in games:
    is_valid = True
    for sub_game in game.sub_games:
        for color in thresholds:
            if sub_game[color] > thresholds[color]:
                is_valid = False
    if is_valid:
        res += game.id
print(res)

res = 0
for game in games:
    is_valid = True
    cur = 1
    for color in thresholds:
        cur *= max([_[color] for _ in game.sub_games])

    res += cur
print(res)
