
with open("input2.txt") as file:
    lines = file.readlines()


tail = [(0,0)]*10
visited = {(0,0)}

dirs = {
    "R": (0,1),
    "L": (0,-1),
    "U": (-1,0),
    "D": (1,0)
}
def sign(v):
    if v > 0: return 1
    if v == 0: return 0
    return -1

for line in lines:
    direction, steps = line.strip().split(" ")
    direction = dirs[direction]

    for _ in range(int(steps)):
        tail[0] = (tail[0][0]+direction[0], tail[0][1]+direction[1])
        for i in range(1,len(tail)):
            if abs(tail[i-1][0]-tail[i][0]) <= 1 and abs(tail[i-1][1]-tail[i][1]) <= 1:
                pass
            else:
                d0 = sign(tail[i-1][0] - tail[i][0])
                d1 = sign(tail[i-1][1] - tail[i][1])
                tail[i] = (tail[i][0]+d0, tail[i][1]+d1)
        visited.add(tail[-1])

print(len(visited))

