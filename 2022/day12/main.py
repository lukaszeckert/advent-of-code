with open("input2.txt") as file:
    lines = file.readlines()
heights = [list(_.strip()) for _ in lines]

n = len(heights)
m = len(heights[0])

[start], [end] = [[(i, j) for i, row in enumerate(heights) for j, cur in enumerate(row) if cur == ch] for ch in
                  ("S", "E")]

heights[start[0]][start[1]] = "a"
heights[end[0]][end[1]] = "z"
dist = [[float("inf") for _ in range(m)] for _ in range(n)]

qu = []
qu_poz = 0
for pos in [(i, j) for i, row in enumerate(heights) for j, cur in enumerate(row) if cur == 'a']:
    dist[pos[0]][pos[1]] = 0
    qu.append(pos)

while qu_poz < len(qu):
    cur = qu[qu_poz]
    qu_poz += 1

    for n_p in [(cur[0] + 1, cur[1]), (cur[0] - 1, cur[1]), (cur[0], cur[1] + 1), (cur[0], cur[1] - 1)]:
        if not (0 <= n_p[0] < n and 0 <= n_p[1] < m):
            continue

        if dist[n_p[0]][n_p[1]] == float("inf") and ord(heights[cur[0]][cur[1]]) + 1 >= ord(
                heights[n_p[0]][n_p[1]]):
            dist[n_p[0]][n_p[1]] = dist[cur[0]][cur[1]] + 1
            qu.append(n_p)

print(dist[end[0]][end[1]])
