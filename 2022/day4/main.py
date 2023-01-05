with open("input2.txt") as file:
    lines = file.readlines()

res = 0

for line in lines:
    first_pair, second_pair = line.split(",")
    first_b,first_e = map(int, first_pair.split("-"))
    second_b, second_e = map(int, second_pair.split("-"))

    if first_b <= second_b and first_e >= second_e:
        res += 1
    elif second_b <= first_b and second_e >= first_e:
        res += 1

print(res)