import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day14inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day14input.txt")) as f:
    data = f.read().strip()


def getstartmap(data):
    lazymap = {}
    rockpaths = []
    for line in data.splitlines():
        rocks = [
            tuple([int(rockstr) for rockstr in r.split(",")])
            for r in line.split(" -> ")
        ]
        for rock, nextrock in zip(rocks, rocks[1:]):
            if rock[0] == nextrock[0]:
                starty = min(rock[1], nextrock[1])
                endy = max(rock[1], nextrock[1])
                for i in range(starty, endy + 1):
                    lazymap[(rock[0], i)] = "█"
            if rock[1] == nextrock[1]:
                starty = min(rock[0], nextrock[0])
                endy = max(rock[0], nextrock[0])
                for i in range(starty, endy + 1):
                    lazymap[(i, rock[1])] = "█"
    return lazymap


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
                print(".", end="")
        print()
    print()


printmap(getstartmap(data))

minx, maxx, miny, maxy = getrange(getstartmap(data))

sandstart = (500, 0)


def trydown(loc, lazymap, p2=False):
    assert loc not in lazymap
    x, y = loc
    if x > maxx or x < minx or y > maxy:
        return "fallen off the earth"
    if (x, y + 1) not in lazymap:
        return trydown((x, y + 1), lazymap)
    if (x - 1, y + 1) not in lazymap:
        return trydown((x - 1, y + 1), lazymap)
    if (x + 1, y + 1) not in lazymap:
        return trydown((x + 1, y + 1), lazymap)
    if loc == (500, 0):
        return "sand is blocking the input"
    return loc  # final resting place


# p1
lazymap = getstartmap(data)
while True:
    result = trydown(sandstart, lazymap)
    # print(result)
    if result == "fallen off the earth":
        break
    lazymap[result] = "o"
    # printmap(lazymap)
    # break
printmap(lazymap)
print(len([1 for x in lazymap.values() if x == "o"]))


# p2

lazymap = getstartmap(data)
for x in range(minx - maxy - 3, maxx + maxy + 3):
    lazymap[(x, maxy + 2)] = "F"  # "█"
minx, maxx, miny, maxy = getrange(lazymap)
printmap(lazymap)

while True:
    result = trydown(sandstart, lazymap)
    # print(result)
    if result == "fallen off the earth":
        break
    if result == "sand is blocking the input":
        lazymap[sandstart] = "o"
        break
    lazymap[result] = "o"
    # printmap(lazymap)
    # break
printmap(lazymap)
print(len([1 for x in lazymap.values() if x == "o"]))
