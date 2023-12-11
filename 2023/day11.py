import numpy as np
import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day11inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day11input.txt")) as f:
    data = f.read().strip()

skymap = []
for line in data.splitlines():
    skymap.append([*line])
    if all(c == "." for c in line):
        skymap.append([*line])

skymap2 = [[] for _ in range(len(skymap))]

for x in range(len(skymap[0])):
    alldots = True
    for y in range(len(skymap)):
        skymap2[y].append(skymap[y][x])
        if skymap[y][x] != ".":
            alldots = False
    if alldots:
        for y in range(len(skymap)):
            skymap2[y].append(skymap[y][x])

    # if all(skymap[c] == "." for c in skymap[])
# for line in data.split("\n\n"):
# print(skymap)
# print(np.array(skymap))
# print(np.array(skymap2))
gallocs2 = []
for y, line in enumerate(skymap2):
    for x, char in enumerate(line):
        if char == "#":
            gallocs2.append((x, y))
# print(gallocs)


def manhat(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


accum = 0
for loc1 in gallocs2:
    for loc2 in gallocs2:
        accum += manhat(*loc1, *loc2)
print("p1:", accum // 2)

#### part2 
skymap_intial = []
for line in data.splitlines():
    skymap_intial.append([*line])

gallocs1 = []
for y, line in enumerate(skymap_intial):
    for x, char in enumerate(line):
        if char == "#":
            gallocs1.append((x, y))

expansion_factor = 1000000
gallocs3 = []
for (g1x, g1y), (g2x, g2y) in zip(gallocs1, gallocs2):
    expandedx = ((g2x - g1x) * (expansion_factor - 1)) + g1x
    expandedy = ((g2y - g1y) * (expansion_factor - 1)) + g1y
    gallocs3.append((expandedx, expandedy))

# print(gallocs1)
# print(gallocs2)
# print(gallocs3)

accum = 0
for loc1 in gallocs3:
    for loc2 in gallocs3:
        accum += manhat(*loc1, *loc2)
print("p2:", accum // 2)
