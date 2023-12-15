
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day15inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day15input.txt")) as f:
    data = f.read().strip()


def makehash(instr):
    accum = 0
    for char in instr:
        accum += ord(char)
        accum *= 17
        accum = accum % 256
    return accum

# print(makehash("HASH"))


bigaccum = 0
for part in data.split(","):
    h = makehash(part)
    # print(part,h)
    bigaccum += h
print("p1:", bigaccum)

import collections
hashmap = collections.defaultdict(dict)

for part in data.split(","):
    if "=" in part:
        loc, focallength = part.split("=")
        h = makehash(loc)
        hashmap[h][loc] = focallength
    elif "-" in part:
        loc, _ = part.split("-")
        h = makehash(loc)
        if loc in hashmap[h]:
            del hashmap[h][loc]
    # print(part)
    # print(hashmap)

score = 0
for boxnr, contents in hashmap.items():
    # dictionaries preserve insertion order
    for slotnr, (loc, focallength) in enumerate(contents.items()):
        s = (boxnr + 1) * (slotnr + 1) * int(focallength)
        # print(loc, slotnr, focallength, s)
        score += s
print("p2:", score)
