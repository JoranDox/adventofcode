
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day14inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day14input.txt")) as f:
    data = f.read().strip()

rounded_rocks = set()
square_rocks = set()
for y, line in enumerate(data.splitlines()):
    for x, char in enumerate(line):
        if char == "O":
            rounded_rocks.add((x,y))
        if char == "#":
            square_rocks.add((x,y))

maxx = x
maxy = y

north = (0, -1)
west = (-1, 0)
south = (0, 1)
east = (1, 0)
directions = [north, west, south, east]

def godirection(x,y,direction):
    return x + direction[0], y + direction[1]

def legal(x,y):
    # x,y = godirection(x,y,direction)
    if x >= 0 and y >= 0 and x <= maxx and y <= maxy:
        return x,y
    return None


def sort_rocks(rocks,direction):
    if direction == north:
        # order by y, ascending
        return sorted(rocks, key=lambda x: x[1])
    if direction == south:
        # order by y, descending
        return sorted(rocks, key=lambda x: x[1], reverse=True)
    if direction == west:
        # order by x, ascending
        return sorted(rocks)
    if direction == east:
        # order by x, descending
        return sorted(rocks, reverse=True)

def moveall(rounded_rocks, direction):
    # part 1
    final_rocks = set()
    accum = 0
    for (x,y) in sort_rocks(rounded_rocks, direction):
        tx = x
        ty = y
        nx, ny = godirection(x,y,direction)
        while (
                ((nx, ny) not in final_rocks)
            and ((nx, ny) not in square_rocks)
            and (legal(nx,ny))
        ):
            tx, ty = nx, ny
            nx, ny = godirection(nx, ny,direction)
        final_rocks.add((tx, ty))
        accum += maxy - ty +1
    return final_rocks, accum
_, accum = moveall(rounded_rocks, north)

def extrapolate(accum, goto=1000000000):
    p = print if accum == 64 else lambda *x, **y: None
    xs = numsseen[accum][-10:]
    cycle = xs[-1]
    p(accum, xs)
    if len(xs) < 10:
        return False
    diffs = [x2 - x1 for x1, x2 in zip(xs[:-1], xs[1:])]
    p(diffs)
    if all([d == diffs[0] for d in diffs]):
        p("yes")
        p(goto - cycle)
        p((goto - cycle -1) % diffs[0])
        if (goto - cycle -1) % diffs[0] == 0:
            p("yesyes")
            print("p2:", accum)
            exit()


print("p1:", accum)
import collections
numsseen = collections.defaultdict(list)
new_rr = rounded_rocks
for cycle in range(10000):
    for direction in directions:
        new_rr, accum = moveall(new_rr, direction)

    numsseen[accum].append(cycle)

    # print("cycle:", cycle, accum, "seen also in:", numsseen[accum][-10:])
    extrapolate(accum)
