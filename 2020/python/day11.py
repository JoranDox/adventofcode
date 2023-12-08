# floor: "."
# empty seat: "L"
# occupied seat "#"

infilename = "day11inputex.txt"
# infilename = "day11input.txt"

# part1:
# seeing = False
# tolerance = 4
# part2: 2032
seeing = True
tolerance = 5

floormap = []


def printfloormap(floormap):
    # print(floormap)
    print("\n".join("".join(line) for line in floormap))
    print()


with open(infilename) as infile:
    for line in infile:
        floormap.append([char for char in line.strip()])
printfloormap(floormap)
ymax = len(floormap)
xmax = len(floormap[0])


def mapget(floormap, x, y):
    if 0 <= y < ymax and 0 <= x < xmax:
        # print(x,y, floormap[y][x])
        return floormap[y][x]
    else:
        # print(x, y, "no")
        return None


def getneighbours(floormap, x, y):
    ret = []
    for ydiff in range(-1, 2):
        for xdiff in range(-1, 2):
            if ydiff == xdiff == 0:
                continue
            tempx = x + xdiff
            tempy = y + ydiff
            neighbour = mapget(floormap, tempx, tempy)
            # print(f"{neighbour=}")
            if seeing:
                while neighbour is not None and neighbour == ".":
                    tempx += xdiff
                    tempy += ydiff
                    neighbour = mapget(floormap, tempx, tempy)

            if neighbour is not None:
                # print("appending")

                ret.append(neighbour)
    return ret


def change(seat, neighbours):
    if seat == "L" and "#" not in neighbours:
        # print("get full:", seat, neighbours)
        return "#"
    if seat == "#" and sum(1 for x in neighbours if x == "#") >= tolerance:
        # print("get empty:", seat, neighbours)
        return "L"
    # print("same:", seat, neighbours)
    return seat


def nextstep(floormap):
    newmap = []
    for y in range(ymax):
        templst = []
        for x in range(xmax):
            tempval = change(mapget(floormap, x, y), getneighbours(floormap, x, y))

            templst.append(tempval)
        newmap.append(templst)
    return newmap


curr = floormap
last = None
while curr != last:
    last = curr
    printfloormap(curr := nextstep(curr))
printfloormap(curr)
print(sum((sum(1 for y in line if y == "#")) for line in curr))
