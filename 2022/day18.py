
import pathlib
parent_directory = pathlib.Path(__file__).resolve().absolute().parent
# with open(parent_directory.joinpath("day18inputtest.txt")) as f:
with open(parent_directory.joinpath("day18input.txt")) as f:
    data = f.read().strip()

lavablocks = [
    tuple(int(x) for x in line.split(","))
    for line in data.splitlines()
]
# print(lavablocks)
#for line in data.split("\n\n"):

def distance(c1,c2):
    return sum((abs(x1-x2) for x1,x2 in zip(c1,c2)))

def adjacent(c1,c2):
    return distance(c1, c2) == 1

def diagadjacent(c1,c2):
    return all((abs(x1-x2)==1 for x1,x2 in zip(c1,c2)))

def setborders(set1):
    sides = 0
    adjacentsides = 0

    for b1 in set1:
        sides += 6
        for b2 in set1:
            if adjacent(b1, b2):
                adjacentsides += 1

    # print(sides, adjacentsides, sides - adjacentsides)
    return sides - adjacentsides

def setborders_two_sets(set1,set2):
    sides = 0
    for b1 in set1:
        for b2 in set2:
            if adjacent(b1,b2):
                sides += 1
    return sides

print(setborders(lavablocks))

import collections
unseenblocks = collections.deque(frozenset((b,)) for b in lavablocks) # copy as sets
# print(unseenblocks)
def setadjacent(set1, set2):
    for b1 in set1:
        for b2 in set2:
            if adjacent(b1, b2):
                return True
                # return (set1 | set2,)
    return False
    # return (set1, set2)

def setadjacent2(set1, set2):
    for b1 in set1:
        for b2 in set2:
            if adjacent(b1, b2) or diagadjacent(b1,b2):
                return True
                # return (set1 | set2,)
    return False
    # return (set1, set2)

def printsets(theset):
    for line in theset:
        print(line)


seenblocks = {}

maxval = max(max(l) for l in lavablocks) + 1
minval = min(min(l) for l in lavablocks) - 1
air = [(minval,minval,minval)]
# print(minval, maxval)
for ax, ay, az in air:
    for x,y,z in [
        (ax-1, ay, az),
        (ax+1, ay, az),
        (ax, ay-1, az),
        (ax, ay+1, az),
        (ax, ay, az-1),
        (ax, ay, az+1),
    ]:
        if (
            (minval <= x <= maxval)
            and (minval <= y <= maxval)
            and (minval <= z <= maxval)
        ):
            if (x,y,z) not in lavablocks and (x,y,z) not in air:
                air.append((x,y,z))

print(len(air), len(lavablocks), (maxval+1)**3)
print("trappedblocks:", (maxval+1)**3 - len(air) - len(lavablocks))
print(setborders_two_sets(lavablocks, air))

# 2044 too low