with open("input2.txt") as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()
    for i in range(len(line)):
        if len(set(line[i:i+14])) == 14:
            print(i+14)
            break
