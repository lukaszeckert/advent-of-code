import re

with open("data2.in" ) as file:
    lines = file.readlines()
mapping = {
    "eight": 8,
    "five":5,
    "three":3,

    "two":2,
    "one":1,

    "four":4,
    "six":6,
    "seven":7,
    "nine":9,
    "1":1,
    "2":2,
    "3":3,
    "4":4,
    "5":5,
    "6":6,
    "7":7,
    "8":8,
    "9":9,
}
res = 0
for l in lines:
    locations = {}

    for k,v in mapping.items():
        for loc in re.finditer(k, l):
            locations[loc.start()] = v
    numbers = sorted([(k,v) for k,v in locations.items()])
    numbers = [_[1] for _ in numbers]
    cur = int(numbers[0])*10+int(numbers[-1])
    print(l, numbers, cur)
    res += cur
print(res)