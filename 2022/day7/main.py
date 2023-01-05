import re
from dataclasses import dataclass


@dataclass
class File:
    path: str
    size: int

with open("input2.txt") as file:
    lines = file.readlines()

files = []
cur_dir = "/"
cd_re = re.compile("cd (?P<dir>.+)")
ls_file_re = re.compile("(?P<size>\d+) (?P<name>.*)")

i = 0
while i < len(lines):
    line = lines[i].strip()

    if matched := cd_re.search(line):
        i += 1
        cd_dir = matched.group("dir")
        if cd_dir[0] == "/":
            cur_dir = cd_dir
        elif cd_dir == "..":
            cur_dir = '/'.join(cur_dir.split("/")[:-2])+"/"
        else:
            cur_dir += cd_dir + "/"

    elif line == "$ ls":
        i += 1
        while i < len(lines) and lines[i][0] != '$':
            line = lines[i].strip()
            if matched := ls_file_re.search(line):
                files.append(File(cur_dir+matched.group("name"), int(matched.group("size"))))
            i += 1

    else:
        print(line)

dir_size = {}
for file in files:
    cur_dir = '/'.join(file.path.split("/")[:-1])+"/"
    print(file.path, cur_dir)
    while True:
        dir_size[cur_dir] = dir_size.get(cur_dir, 0) + file.size
        if cur_dir == "/":
            break

        cur_dir = '/'.join(cur_dir.split("/")[:-2])+"/"

print(sum([v for k,v in dir_size.items() if v < 100000]))
needed_space = 30000000-(70000000-dir_size["/"])

res_value = float("inf")
res_size = 0
for v in dir_size.values():
    if v >= needed_space and v < res_value:
        print(v)
        res_value = v
print(res_value, res_size, needed_space)
