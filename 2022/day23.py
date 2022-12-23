
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day23inputtestsmall.txt")) as f:
# with open(aoc_dir.joinpath("input/2022/day23inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day23input.txt")) as f:
    data = f.read().strip()

elfmap = {}
for y, line in enumerate(data.splitlines()):
    for x, char in enumerate(line):
        if char in ("#"):
            elfmap[(x,y)] = 0

def getrange(lazymap):
    xonly = [r[0] for r in lazymap]
    yonly = [r[1] for r in lazymap]
    minx, maxx = min(xonly), max(xonly)
    miny, maxy = min(yonly), max(yonly)
    return minx, maxx, miny, maxy

def printmap(lazymap):
    minx, maxx, miny, maxy = getrange(lazymap)
    counter = 0
    for y in range(miny, maxy+1):
        # print(y)
        for x in range(minx, maxx+1):
            # print(x)
            if (x,y) in lazymap:
                print(lazymap[(x,y)],end="")
            else:
                counter += 1
                print(".",end="")
        print()
    print()
    return counter

printmap(elfmap)

def neg(v):
    return tuple(-x for x in v)

def vsum(*v):
    return tuple(sum(x) for x in zip(*v))

def vmul(v, num):
    return tuple(int(vx * num) for vx in v)

directions = [
    ( 0, -1), # "N"
    ( 0,  1), # "S"
    (-1,  0), # "W"
    ( 1,  0), # "E"
]

eightdirections = [
    ( 1,-1), # NE
    ( 1, 0), # E
    ( 1, 1), # SE
    ( 0, 1), # S
    ( 0,-1), # N
    (-1,-1), # NW
    (-1, 0), # W
    (-1, 1), # SW
]
print(directions)

def ish(direction):
    x,y = direction
    if x == 0:
        return (
            (-1, y),
            ( 0, y),
            ( 1, y),
        )
    else:
        assert y == 0
        return (
            (x, -1),
            (x,  0),
            (x,  1),
        )

numrounds = 0
initialdirection = -1
while True:
    print(numrounds)
    initialdirection += 1
    numrounds += 1
    happyelves = set()
    allelveshappy = True
    for elf in elfmap:
        thiselfhappy = True
        for neighbour in eightdirections:
            if vsum(elf,neighbour) in elfmap:
                allelveshappy = False
                thiselfhappy = False
                break

        if thiselfhappy:
            happyelves |= {elf}

    if allelveshappy:
        # we done here
        print("all elves happy")
        break

    # printmap(elfmap)

    proposals = {}
    for location, _ in elfmap.items():
        # print("checking for", location)
        if location in happyelves:
            # print(location, "is a happy elf")
            proposals[location] = (location, initialdirection)
            # print("proposing", proposals[location])
        else:
            for i in range(4):
                direction = directions[(initialdirection + i) % 4]
                okay = True
                for tocheckdirection in ish(direction):
                    if vsum(location,tocheckdirection) in elfmap:
                        okay = False
                        break # don't bother with this direction
                if okay:
                    # print("found a good direction:", direction)
                    proposals[location] = ((vsum(location,direction)), (initialdirection+1)%4)
                    # print("proposing", proposals[location])
                    break # done with this elf
        if location not in proposals:
            # couldn't find a path, keep standing there but start looking in a new direction next
            proposals[location] = (location, (initialdirection+1)%4)
            # print("proposing", proposals[location])

    assert list(elfmap) == list(proposals)
    # print(proposals)
    sortedproposals = sorted([p[0] for p in proposals.values()])
    # print(sortedproposals)
    duplicateproposals = {
        p1
        for p1,p2 in
        zip(sortedproposals, sortedproposals[1:])
        if p1 == p2
    }
    # print(duplicateproposals)

    newelfmap = {}
    for fromloc, (proposedloc, nextdirection) in proposals.items():
        if proposedloc in duplicateproposals:
            newelfmap[fromloc] = nextdirection
        else:
            newelfmap[proposedloc] = nextdirection
    # printmap(newelfmap)

    assert len(newelfmap) == len(elfmap) # make sure we don't lose any elves
    elfmap = newelfmap


    if numrounds == 10:
        print("p1:", printmap(elfmap))
    # else:
    #     printmap(elfmap)

    # break
print("p2:", numrounds)
