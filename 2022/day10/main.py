
with open("input2.txt") as file:
    lines = file.readlines()

X = 1
cycle = 0
res = 0
row = ""

for line in lines:
    line = line.strip()
    d_x = 0
    if line == "noop":
        d_cycle = 1
    else:
        d_x = int(line.split(" ")[-1])
        d_cycle = 2

    for _ in range(d_cycle):
        if (cycle+1-20)%40 == 0:
            res += (cycle+1)*X

        if abs(len(row)-X) < 2:
            row += "#"
        else:
            row += " "
        if len(row) == 40:
            print(row)
            row = ""

        cycle += 1

    X += d_x
print(res)
