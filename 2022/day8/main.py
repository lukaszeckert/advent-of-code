
with open("input2.txt") as file:
    lines = file.readlines()

data = [list(map(int, _.strip())) for _ in lines]
n = len(data)
m = len(data)
res = float(0)

def find_score(data, row, col):
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    val = data[row][col]
    res = 1
    for dir in dirs:
        cur_r = row+dir[0]
        cur_c = col+dir[1]
        while 0 <= cur_r < len(data) and 0 <= cur_c < len(data[0]) and data[cur_r][cur_c] < val:
            cur_r += dir[0]
            cur_c += dir[1]
        res *= abs(min(len(data)-1, max(cur_r, 0))-row)+abs(min(max(cur_c,0), len(data[0])-1)-col)
    return res

print(find_score(data, 3, 2))

# tmp = []
for r in range(n):
    tmp_r = []
    for c in range(m):
        score = find_score(data, r, c)
        tmp_r.append(score)
        res = max(score, res)
    print(tmp_r)
print(res)
# visible = [[False for _ in range(m)] for _ in range(n)]
#
# for r in range(n):
#     max_height = float("-inf")
#     for c in range(m):
#         if data[r][c] > max_height:
#             visible[r][c] = True
#         max_height = max(max_height, data[r][c])
#     max_height = float("-inf")
#     for c in reversed(range(m)):
#         if data[r][c] > max_height:
#             visible[r][c] = True
#         max_height = max(max_height, data[r][c])
#
# for c in range(m):
#     max_height = float("-inf")
#     for r in range(n):
#         if data[r][c] > max_height:
#             visible[r][c] = True
#         max_height = max(max_height, data[r][c])
#     max_height = float("-inf")
#     for r in reversed(range(n)):
#         if data[r][c] > max_height:
#             visible[r][c] = True
#         max_height = max(max_height, data[r][c])


print(visible)
print(sum(sum(_) for _ in visible))