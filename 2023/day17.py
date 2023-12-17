# slow code, don't copy :c

import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day17inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day17input.txt")) as f:
    data = f.read().strip()


north = (0, -1)
west = (-1, 0)
south = (0, 1)
east = (1, 0)

def inverse(direction):
    x,y = direction
    return (-x, -y)

def godirection(loc,direction):
    x,y = loc
    return x + direction[0], y + direction[1]

def legal(loc):
    x,y = loc
    # x,y = godirection(x,y,direction)
    if x >= 0 and y >= 0 and x <= maxx and y <= maxy:
        return x,y
    return None

def mapprint(m):
    for y in range(maxy+1):
        for x in range(maxx+1):
            print(m.get((x,y), " "), end=" ")
        print()

heatmap = {}

for y, line in enumerate(data.splitlines()):
    for x, char in enumerate(line):
        heatmap[(x,y)] = int(char)


maxx = x
maxy = y
print(maxx,maxy)

# mapprint(heatmap)

bestlocs = {((0,0),east,0): 0}
tocheck = [((0,0),east,0,0)]

def getoptions(loc,prevdirection,stepsinthatdirection,cost):
    # print("enter getoptions with", loc,prevdirection,stepsinthatdirection,cost)
    legaldirs = [
        (nxy,direction)
        for direction in (north,west,south,east)
        if (
            (
                stepsinthatdirection < 3
                or prevdirection != direction
            )
            and legal(nxy:=godirection(loc,direction))
            and direction != inverse(prevdirection)
        )
    ]
    # print("legal",legaldirs)
    ret = [
        (nxy, direction, (stepsinthatdirection + 1 if direction == prevdirection else 1), cost+heatmap[nxy])
        for nxy, direction in legaldirs
    ]
    # print("ret",ret)
    return ret

def getoptionsp2(loc,prevdirection,stepsinthatdirection,cost):
    # print("enter getoptions with", loc,prevdirection,stepsinthatdirection,cost)
    legaldirs = [
        (nxy,direction)
        for direction in (north,west,south,east)
        if (
            # must be legal always
            legal(nxy:=godirection(loc,direction))
            # can't invert
            and direction != inverse(prevdirection)
            and (
                # can only keep going straight for 10 steps max
                (prevdirection == direction and stepsinthatdirection < 10)
                or
                # can't turn before 4 steps
                (prevdirection != direction and stepsinthatdirection >= 4)
            )
        )
    ]
    # print("legal",legaldirs)
    ret = [
        (nxy, direction, (stepsinthatdirection + 1 if direction == prevdirection else 1), cost+heatmap[nxy])
        for nxy, direction in legaldirs
    ]
    # print("ret",ret)
    return ret

minseen = None
wannaprint = 1
iterations = 0
while tocheck:
    iterations += 1
    if iterations % 10 == 0:
        print("iters:", iterations)
    options = [
        opt
        for check in tocheck
        for opt in getoptions(*check)
    ]
    # print("options:",options)
    tocheck = []
    for loc,prevdirection,stepsinthatdirection,cost in options:
        if (loc,prevdirection,stepsinthatdirection) not in bestlocs or cost < bestlocs[(loc,prevdirection,stepsinthatdirection)]:
            tocheck.append((loc,prevdirection,stepsinthatdirection,cost))
            bestlocs[(loc,prevdirection,stepsinthatdirection)] = cost
            if loc == (maxx, maxy):
                if not minseen or minseen > cost:
                    minseen = cost
                    print("best final seen until now:", cost)
    # print("tocheck",tocheck)
    # mapprint({loc:cost for ((loc,prevdirection,stepsinthatdirection),cost) in bestlocs.items()})



