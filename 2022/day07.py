import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day07inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day07input.txt")) as f:
    data = f.read().strip()


dirs = {
    "/": {
        # "type": "directory",
        "type": "d",
        "size": 0,
        "parent_directory": (),
    }
}
dirlist = []
filelist = []


def tpath(dic, tup):
    # print(dic)
    # print(tup)
    cwd = dic
    for t in tup:
        cwd = cwd[t]
    return cwd


path = tuple()

to_consume = data.splitlines()
while to_consume:
    # print(dirs)
    line, to_consume = to_consume[0], to_consume[1:]
    # print(line)
    if line.startswith("$ cd .."):
        # print("changing path")
        path = path[:-1]
        # print(path)
    elif line.startswith("$ cd"):
        # print("changing path")
        _, _, dirname = line.split()
        path = path + (dirname,)
        # print(path)
    elif line.startswith("$ ls"):
        while to_consume and (not to_consume[0].startswith("$")):
            subline, to_consume = to_consume[0], to_consume[1:]
            # print("    ", subline)
            dir_or_number, name = subline.split()
            if dir_or_number == "dir":
                # print("adding dir", name)
                newdir = {
                    # "type": "directory",
                    "type": "d",
                    "size": 0,
                    "parent_directory": path,
                }
                tpath(dirs, path)[name] = newdir
                dirlist.append((name, newdir))
            else:
                # print("adding file", name)
                newfile = {
                    # "type": "file",
                    "type": "f",
                    "size": int(dir_or_number),
                    "parent_directory": path,
                }
                tpath(dirs, path)[name] = newfile
                filelist.append((name, newfile))

                temppath = path
                while temppath:
                    tpath(dirs, temppath)["size"] += int(dir_or_number)
                    temppath = tpath(dirs, temppath)["parent_directory"]
import json

# print(json.dumps(dirs,indent=4))
# print(dirlist)

# for line in data.split("\n\n"):


print("p1:", sum([(size["size"]) for name, size in dirlist if size["size"] < 100_000]))

total_size = 70_000_000
size_needed = 30_000_000
size_used = dirs["/"]["size"]
size_unused = total_size - size_used
minimum_size_to_delete = size_needed - size_unused

mindirsize = min(
    [(size["size"]) for name, size in dirlist if size["size"] > minimum_size_to_delete]
)

print(
    "p2:",
    mindirsize,
)
