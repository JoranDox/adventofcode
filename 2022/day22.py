import collections
import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day22inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day22input.txt")) as f:
    data = f.read()

# for line in data.splitlines():
board, instructions = data.split("\n\n")

boardmap = {}
for y, line in enumerate(board.splitlines()):
    for x, char in enumerate(line):
        if char in ("oO.#"):
            boardmap[(x, y)] = char


def getrowrange(lazymap, x):
    yonly = [r[1] for r in lazymap if r[0] == x]
    return min(yonly), max(yonly)


def getcolrange(lazymap, y):
    xonly = [r[0] for r in lazymap if r[1] == y]
    return min(xonly), max(xonly)


def getrange(lazymap):
    xonly = [r[0] for r in lazymap]
    yonly = [r[1] for r in lazymap]
    minx, maxx = min(xonly), max(xonly)
    miny, maxy = min(yonly), max(yonly)
    return minx, maxx, miny, maxy


def printmap(lazymap):
    minx, maxx, miny, maxy = getrange(lazymap)

    for y in range(miny - 1, maxy + 2):
        # print(y)
        for x in range(minx - 1, maxx + 2):
            # print(x)
            if (x, y) in lazymap:
                print(lazymap[(x, y)], end="")
            else:
                print(" ", end="")
        print()
    print()


printmap(boardmap)

minx, maxx, miny, maxy = getrange(boardmap)
print(minx, maxx, miny, maxy)

directions = [
    (1, 0),  # right
    (0, 1),  # down
    (-1, 0),  # left
    (0, -1),  # up
]

eightdirections = [
    (1, -1),  # right
    (1, 0),  # right
    (1, 1),  # right
    (0, 1),  # down
    (0, -1),  # up
    (-1, -1),  # left
    (-1, 0),  # left
    (-1, 1),  # left
]

directionstoprint = [
    ">",  # right
    "v",  # down
    "<",  # left
    "^",  # up
]


def neg(v):
    return tuple(-x for x in v)


def vsum(*v):
    return tuple(sum(x) for x in zip(*v))


def vmul(v, num):
    return tuple(int(vx * num) for vx in v)


currentdirection = 0
firstrowrange = getcolrange(boardmap, 0)
print(firstrowrange)
startposition = (firstrowrange[0], 0)
print(startposition)
print(boardmap)
assert startposition in boardmap


def nextpos(lazymap, location, direction):
    suggested = vsum(location, directions[direction])
    if suggested not in lazymap:
        # loop around
        temploc = location
        while temploc in lazymap:
            # print("looping around:", temploc)
            temploc = vsum(temploc, neg(directions[direction]))
        suggested = vsum(temploc, directions[direction])
        assert suggested in lazymap

    if lazymap[suggested] == "#":
        return location
    else:
        return suggested


# print(instructions)


def parseinstructionstring(instructions):
    current = []
    for char in instructions:
        if char in ["R", "L"]:
            # print(f"joining {current} into a number")
            yield int("".join(current))
            yield char
            current = []
        elif char in str(list(range(10))):
            current.append(char)
        else:
            print(f'huh? "{char}"')
    if current:
        yield int("".join(current))


# print(list(parseinstructionstring(instructions)))

currentposition = startposition
for instruction in parseinstructionstring(instructions):
    # print(instruction, currentposition, currentdirection)
    if instruction == "R":
        # print("dir:", currentdirection, end="")
        currentdirection = (currentdirection + 1) % 4
        # print("->", currentdirection)
    elif instruction == "L":
        # print("dir:", currentdirection, end="")
        currentdirection = (currentdirection + 3) % 4  # -1
        # print("->", currentdirection)
    else:
        for i in range(instruction):
            boardmap[currentposition] = directionstoprint[currentdirection]
            currentposition = nextpos(boardmap, currentposition, currentdirection)
            # print(currentposition)


printmap(boardmap)

x, y = currentposition
print("p1:", (y + 1) * 1000 + (x + 1) * 4 + currentdirection)

############################## p2

cubemap = {}
for y, line in enumerate(board.splitlines()):
    for x, char in enumerate(line):
        if char in ("oO.#"):
            cubemap[(x, y)] = char

# Top/Under, Right/Left, Forward/Backward
cube = {
    # neighbours rotating clockwise
    "T": ["B", "L", "F", "R"],
    "B": ["R", "U", "L", "T"],
    "U": ["R", "F", "L", "B"],
    "F": ["R", "T", "L", "U"],
    "L": ["U", "F", "T", "B"],
    "R": ["T", "F", "U", "B"],
}


def printableside(side, rot):
    return (
        f" {cube[side][(rot+3)%4]} ",
        f"{cube[side][(rot+2)%4]}{side}{cube[side][(rot)%4]}",
        f" {cube[side][(rot+1)%4]} ",
    )


# print("\n".join(printableside("T", 0)))
# print("\n".join(printableside("T", 1)))
# print("\n".join(printableside("T", 2)))
# print("\n".join(printableside("T", 3)))
sidesize = int((len(cubemap) / 6) ** (0.5))
print(sidesize)


def reducesize(cubemap):
    ret = {}
    first = False
    for y in range(6):
        for x in range(6):
            if (x * sidesize, y * sidesize) in cubemap:
                if not first:
                    ret[(x, y)] = "T"
                    first = (x, y)  # truthy whatever is in there
                else:
                    ret[(x, y)] = "?"
    return ret, first


smallermap, top = reducesize(cubemap)
printmap(smallermap)


def assignsides(smallermap):
    allsides = {"F", "B", "T", "U", "R", "L"}
    known = set()
    fixedrotations = {}
    while known < allsides:
        for side in allsides - known:
            locs = [k for k, v in smallermap.items() if v == side]
            if locs:
                assert len(locs) == 1  # no duplicates
                locx, locy = locs[0]
                for rot in range(4):
                    printmap(smallermap)
                    # print("comparing")
                    # print("\n".join(printableside(side, rot)))
                    # expected = printableside(side, rotation)
                    count_ok = 0
                    potential = {}
                    #                         cube[side][(rot+i+3)%4]
                    # cube[side][(rot+i+2)%4]          side           cube[side][(rot+i)%4]
                    #                         cube[side][(rot+i+1)%4]
                    #                     (locx, locy-1)
                    # (locx-1, locy)      (locx, locy)        (locx+1, locy)
                    #                     (locx, locy+1)
                    # print(list(zip(
                    #     [
                    #         smallermap.get((locx+1, locy)),
                    #         smallermap.get((locx, locy+1)),
                    #         smallermap.get((locx-1, locy)),
                    #         smallermap.get((locx, locy-1)),
                    #     ],
                    #     (cube[side] + cube[side])[rot:], # rotated side
                    # )))
                    for loc, expected in zip(
                        [
                            (locx + 1, locy),
                            (locx, locy + 1),
                            (locx - 1, locy),
                            (locx, locy - 1),
                        ],
                        (cube[side] + cube[side])[rot:],
                    ):
                        if loc in smallermap:
                            if smallermap[loc] == expected:
                                count_ok += 1
                            else:
                                potential[loc] = expected
                    if count_ok > 0 or (side == "T"):
                        # good, let's apply
                        # print("yes, got", side)
                        known |= {side}
                        fixedrotations[side] = rot
                        for k, v in potential.items():
                            smallermap[k] = v
                        # printmap(smallermap)
    return fixedrotations


fixedrotations = assignsides(smallermap)
print(fixedrotations)
for s, r in fixedrotations.items():
    print(f"side {s}:")
    print("\n".join(printableside(s, r)))
    print()


printmap(smallermap)


def enlarge(smallermap, cubemap):
    return {(x, y): smallermap[(x // sidesize, y // sidesize)] for x, y in cubemap}


sidesmap = enlarge(smallermap, cubemap)
printmap(sidesmap)

reversesidesmap = {v: k for k, v in sidesmap.items()}
reversesmallermap = {v: k for k, v in smallermap.items()}


def rotateleft(loc, steps=1):
    lx, ly = loc
    lx -= (sidesize - 1) / 2
    ly -= (sidesize - 1) / 2
    while steps:
        steps -= 1
        lx, ly = ly, -lx
    lx += (sidesize - 1) / 2
    ly += (sidesize - 1) / 2
    return int(lx), int(ly)


def rotateright(loc, steps=1):
    lx, ly = loc
    lx -= (sidesize - 1) / 2
    ly -= (sidesize - 1) / 2
    while steps:
        steps -= 1
        lx, ly = -ly, lx
    lx += (sidesize - 1) / 2
    ly += (sidesize - 1) / 2
    return int(lx), int(ly)


# testcount = 0


def nextposoncube(lazymap, location, direction):
    global testcount
    assert location in lazymap
    assert location in sidesmap
    suggested = vsum(location, directions[direction])
    nextdirection = direction
    if suggested not in lazymap:
        # testcount -= 1
        # if testcount < 0:
        #     print(testcount)
        #     dprint = print
        #     dprintmap = printmap
        # else:
        dprint = lambda *x: True
        dprintmap = lambda *x: None
        dprintmap(lazymap)
        # go around cube, find new suggested location & potentially change direction
        currentside = sidesmap[location]
        dprint("current side:", currentside)
        dprint("falling off direction:", direction, directions[direction])
        dprint(fixedrotations)
        localmap = printableside(currentside, fixedrotations[currentside])
        dprint("local map:")
        dprint("\n".join(localmap))
        nx, ny = vsum((1, 1), directions[direction])
        nextside = localmap[ny][nx]
        dprint("next side:", nextside)

        nextlocalmap = printableside(nextside, fixedrotations[nextside])
        dprint("next local map:")
        dprint("\n".join(nextlocalmap))
        for testdirection, (dx, dy) in enumerate(directions):
            if nextlocalmap[1 - dy][1 - dx] == currentside:
                nextdirection = testdirection
                dix, diy = dx, dy

        dprint("next direction:", nextdirection, (dix, diy))
        topleftx, toplefty = reversesmallermap[currentside]
        dprint(
            "topleft at",
            (topleftx, toplefty),
            "=",
            (topleftx * sidesize, toplefty * sidesize),
        )
        relx, rely = vsum(location, neg((topleftx * sidesize, toplefty * sidesize)))

        dprint(
            "pos, topleft, rel pos",
            location,
            (topleftx * sidesize, toplefty * sidesize),
            (relx, rely),
        )
        normalisedposition = rotateleft((relx, rely), direction + 1)
        dprint("norm pos:", normalisedposition)
        assert normalisedposition[1] == 0
        invpos = (sidesize - 1 - normalisedposition[0], 0)
        dprint("incoming normalised pos:", invpos)
        nextdenormalisedposition = rotateright(invpos, nextdirection + 3)
        dprint("nextdenormalisedposition:", nextdenormalisedposition)

        nexttopleftx, nexttoplefty = reversesmallermap[nextside]
        dprint(
            "nexttopleft at",
            (nexttopleftx, nexttoplefty),
            "=",
            (nexttopleftx * sidesize, nexttoplefty * sidesize),
        )
        suggested = vsum(
            nextdenormalisedposition, (nexttopleftx * sidesize, nexttoplefty * sidesize)
        )
        dprint("suggested", suggested)

        assert dprint()

    assert suggested in lazymap
    if lazymap[suggested] == "#":
        # print("wall")
        return location, direction  # can't move, wall in the way
    else:
        return suggested, nextdirection


# print(nextposoncube(boardmap,startposition, 0))

currentposition = startposition
currentdirection = 0
for instruction in parseinstructionstring(instructions):
    # print("-- instruction:", instruction, currentposition, currentdirection)
    if instruction == "R":
        # print("dir:", currentdirection, end="")
        currentdirection = (currentdirection + 1) % 4
        # print("->", currentdirection)
    elif instruction == "L":
        # print("dir:", currentdirection, end="")
        currentdirection = (currentdirection + 3) % 4  # -1
        # print("->", currentdirection)
    else:
        for i in range(instruction):
            cubemap[currentposition] = directionstoprint[currentdirection]
            currentposition, currentdirection = nextposoncube(
                cubemap, currentposition, currentdirection
            )
            # print(currentposition, currentdirection)

# 21227 is too low
# 162096
x, y = currentposition
print("p2:", (y + 1) * 1000 + (x + 1) * 4 + currentdirection)


# # def assignside(smallermap):
# #     sidesize = int((len(cubemap) / 6) ** (.5))
# #     print(sidesize)
# #     sidemap = {}
# #     reducedmap = {}
# #     allsides = {"F","B", "T","U", "R","L"}
# #     known = {"T"}
# #     initialpos = (getcolrange(cubemap, 0)[0],0) # top left
# #     # per definition, initial pos == T
# #     sidemap[initialpos] = "T"
# #     for y in range(sidesize):
# #         for x in range(sidesize):
# #             sidemap[vsum(initialpos, (x,y))] = "T"

# #     # while known != allsides:
# #     for direction in directions:
# #         newloc = vsum(initialpos, vmul(direction,sidesize))
# #         if newloc in cubemap:
# #             # find out which side it is
# #             for y in range(sidesize):
# #                 for x in range(sidesize):
# #                     sidemap[vsum(initialpos, (x,y))] = "T"


# # assignside(boardmap)
# raise
# def findedges(cubemap):
#     edges = []
#     initialpos = (getcolrange(cubemap, 0)[0],0) # top left
#     position = (getcolrange(cubemap, 0)[0]+1,0) # top left + 1 to the right
#     edges.append(initialpos)
#     edges.append(position)
#     seen = {initialpos, position}
#     found = True
#     startpoints = []
#     beforestart = None
#     while found:
#         found = False
#         for direction in directions:
#             attempt = vsum(position,direction)
#             if attempt not in seen and attempt in cubemap:
#                 emptydirections = [
#                     direction2
#                     for direction2 in directions
#                     if vsum(attempt, direction2) not in cubemap
#                 ]
#                 neighs = len([
#                     direction2
#                     for direction2 in eightdirections
#                     if vsum(attempt, direction2) in cubemap
#                 ])
#                 assert neighs in [3,5,6,7,8], (neighs, attempt, emptydirections)
#                 if neighs < 8:
#                     if neighs == 7:
#                         assert len(emptydirections) == 0, (neighs, attempt, emptydirections)
#                         # inner corner edge, not to be connected but good starting point for later
#                         startpoints.append(attempt)
#                         if beforestart is None:
#                             beforestart = edges
#                             edges = []
#                     elif neighs == 3:
#                         assert len(emptydirections) == 2, (neighs, attempt, emptydirections)
#                         # outer corner edge, connect twice
#                         edges.append((attempt,emptydirections[0]))
#                         edges.append((attempt,emptydirections[1])) # TODO this ordering
#                     elif neighs in [5,6]:
#                         assert len(emptydirections) == 1, (neighs, attempt, emptydirections)
#                         # other edges
#                         # 5 = normal
#                         # 6 = next to inner corner
#                         edges.append((attempt,emptydirections[0]))
#                     seen |= {attempt}
#                     position = attempt
#                     found = True
#                     break
#     print(position)
#     return edges + beforestart, startpoints

# print(findedges(boardmap))

# def connectedges(cubemap):
#     edges, _ = findedges(cubemap)
#     return {
#         x:y
#         for x,y in zip(edges,edges[::-1])
#     }

# print(connectedges(boardmap))

# # first we need to find a location that looks like this empty space with filled in spots to 2 corners:
# #   -->  #
# #       ##
# seen = {}
# edges = {}
# goodstart = None
# for location in cubemap:
#     for direction in directions:
#         attempt = vsum(location, direction)
#         if attempt in seen or attempt in cubemap:
#             continue # don't do things twice and don't look at inner spots
#         else:
#             seen |= attempt
#         ncount = 0
#         for direction2 in directions:
#             if vsum(attempt, direction2) in cubemap:
#                 ncount += 1
#         assert 1 <= ncount <= 2
#         if ncount == 2:
#             # good starting point
