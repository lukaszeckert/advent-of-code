score = 0
with open("input2.txt") as file:
    lines = file.readlines()

for l1,l2,l3 in zip(lines[0::3], lines[1::3], lines[2::3]):
    l1 = set(l1.rstrip())
    l2 = set(l2.rstrip())
    l3 = set(l3.rstrip())

    common = list(l1.intersection(l2).intersection(l3))[0]

    if common >= 'a':
        score += ord(common)-97+1
    else:
        score += ord(common)-65+26+1

print(score)