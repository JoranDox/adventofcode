
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day16inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day16input.txt")) as f:
    data = f.read().strip()

tilemap = {}

for y, line in enumerate(data.splitlines()):
    for x, char in enumerate(line):
        # if char != ".":
        tilemap[(x,y)] = char


maxx = x
maxy = y

north = (0, -1)
west = (-1, 0)
south = (0, 1)
east = (1, 0)

def godirection(x,y,direction):
    return x + direction[0], y + direction[1]

def legal(x,y):
    # x,y = godirection(x,y,direction)
    if x >= 0 and y >= 0 and x <= maxx and y <= maxy:
        return x,y
    return None

def donext(xy,direction):
    n = godirection(*xy,direction)
    if not legal(*n):
        return None
    match tilemap[n]:
        case ".":
            return [(n, direction)]
        case "\\":
            if direction == north:
                return [(n, west)]
            if direction == east:
                return [(n, south)]
            if direction == south:
                return [(n, east)]
            if direction == west:
                return [(n, north)]
        case "/":
            if direction == north:
                return [(n, east)]
            if direction == east:
                return [(n, north)]
            if direction == south:
                return [(n, west)]
            if direction == west:
                return [(n, south)]
        case "-":
            if direction in (east, west):
                return [(n, direction)]
            if direction in (north, south):
                return [
                    (n, east), (n, west)
                ]
        case "|":
            if direction in (north, south):
                return [(n, direction)]
            if direction in (east, west):
                return [
                    (n, north), (n, south)
                ]

    return [(n, direction)]

# print(donext((1,2),north))

def doanattempt(start):
    seen = set()
    newseen = True
    while newseen:
        # print(start)
        start = {
            beam 
            for b in start if (beams:=donext(*b))
            # flatten magic
            for beam in beams
        }
        # print(start)
        # locs = {loc for loc,direction in start}
        if start <= seen:
            newseen = False
        start -= seen
        # print("seen", seen)
        # print(start, "after removal")

        seen |= start

    # print(len(seen))
    seenlocs = {loc for loc,direction in seen}
    return(len(seenlocs))

    # for y in range(maxy+1):
    #     for x in range(maxx+1):
    #         if (x,y) in seenlocs:
    #             print("#", end="")
    #         else:
    #             print(tilemap[(x,y)], end="")
    #     print()
print("p1:", doanattempt(start = [((-1,0), east)]))

bestattempt = 0
for y in range(maxy+1):
    bestattempt = max(bestattempt, doanattempt(
        start = [((-1,y), east)]
    ))
    bestattempt = max(bestattempt, doanattempt(
        start = [((maxx+1,y), west)]
    ))
for x in range(maxx+1):
    bestattempt = max(bestattempt, doanattempt(
        start = [((x, -1), south)]
    ))
    bestattempt = max(bestattempt, doanattempt(
        start = [((x, maxy+1), north)]
    ))
print(bestattempt)
