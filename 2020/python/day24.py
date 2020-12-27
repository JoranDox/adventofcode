from collections import deque
import copy

infilename = "day24input.txt"
# infilename = "day24inputex.txt"
# infilename = "day24inputexinf.txt"

with open(infilename) as infile:
    tilepaths = infile.read().strip().split("\n")

import numpy as np

directions = {
    # 'e'  : np.array((1,0)),
    # 'w'  : np.array((-1,0)),
    # 'se' : np.array((0,-1)),
    # 'nw' : np.array((0,1)),
    # 'ne' : np.array((1,1)),
    # 'sw' : np.array((-1,-1)),
    'e'  : np.array((2,0)),
    'w'  : np.array((-2,0)),
    'se' : np.array((1,-2)),
    'nw' : np.array((-1,2)),
    'ne' : np.array((1,2)),
    'sw' : np.array((-1,-2)),
}

parsedtilepaths = []

for path in tilepaths:
    parsedpath = []
    i = 0
    while i < len(path):
        if path[i] in directions:
            dirn = path[i]
            i += 1
        else:
            dirn = path[i:i+2]
            i += 2
        parsedpath.append(directions[dirn])
    parsedtilepaths.append(parsedpath)
# print([sum(p) for p in parsedtilepaths])

# def canonical(loc):
#     mx = max(loc)
#     mn = min(loc)
#     comp = mx * mn
#     # print(mx,mn,comp)
#     if comp > 0:
#         return loc - (mn,mn,mn)
#     elif comp <= 0:
#         return loc
#     else:
#         raise 1234

countset = set()
for p in parsedtilepaths:
    # print(p)
    # print(sum(p))
    can = tuple(sum(p))
    
    if can in countset:
        countset -= set((can,))
    else:
        countset |= set((can,))
# print(countset)
print(len(countset))

def nextset(inset):
    nextset = copy.copy(inset)
    tocheck = list(copy.copy(inset))
    for tile in inset:
        for dirc in directions.values():
            tocheck.append(tuple(np.array(tile) + dirc))
    for tile in set(tocheck):
        c = 0
        for dirc in directions.values():
            if tuple(np.array(tile) + dirc) in inset:
                c += 1
        # print(tile,c)
        if (tile in inset) and ((c > 2) or (c == 0)):
            # print(f'{tile} removed')
            nextset -= set((tile,))
        if (tile not in inset) and (c == 2):
            # print(f'{tile} added')
            nextset |= set((tile,))
    return nextset

for i in range(100):
    # print(countset)
    print(len(countset))
    countset = nextset(countset)
print(len(countset))