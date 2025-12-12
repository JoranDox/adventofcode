import pathlib
import enum
from collections import abc

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2025/day09inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2025/day09input.txt")) as f:
    data = f.read().strip()

loc = tuple[int, int]


class direction(loc, enum.Enum):
    topleft = (-1, -1)
    topright = (1, -1)
    bottomleft = (-1, 1)
    bottomright = (1, 1)


reds: list[loc] = []
greens: list[loc] = []


def makeline(l1: loc, l2: loc) -> list[loc]:
    rindex = None
    x = None
    y = None
    # print(l1, l2)
    if l1[0] == l2[0]:
        x = l1[0]
        rindex = 1
    elif l1[1] == l2[1]:
        y = l1[1]
        rindex = 0
    assert rindex is not None, rindex
    assert x is not None or y is not None, (x, y)
    ret: list[loc] = []
    for i in range(min(l1[rindex], l2[rindex]), max(l1[rindex], l2[rindex]) + 1):
        if rindex == 0:
            assert y is not None
            ret.append((i, y))
        else:
            assert x is not None
            ret.append((x, i))
    if len(ret) < 3:
        print("oh no")  # this would complicate things if not true

    return ret


def printgrid(
    *printables: tuple[abc.Container[loc], str],
    # reds: set[loc] | list[loc],
    # greens: set[loc] | list[loc],
    # swappables: set[loc],
    # notswappables: set[loc] = set(),
) -> None:
    for y in range(maxy + 1):
        row = ""
        for x in range(maxx + 1):
            for p, c in printables:
                if (x, y) in p:
                    row += c
                    break
            else:
                row += "."
        print(row)


maxx = 0
maxy = 0
minx = None
miny = None
prevx, prevy = map(int, (data.splitlines()[-1].split(",")))
for line in data.splitlines():
    x, y = map(int, line.split(","))
    reds.append((x, y))
    between = makeline((prevx, prevy), (x, y))
    for l in between[1:-1]:  # exclude endpoints
        greens.append(l)
    prevx, prevy = x, y
    if x > maxx:
        maxx = x
    if y > maxy:
        maxy = y
    if minx is None or x < minx:
        minx = x
    if miny is None or y < miny:
        miny = y

maxred = max(reds)
# maxred is definitely a corner with the inside to the top left


def locdiff(l1: loc, l2: loc) -> loc:
    return (l1[0] - l2[0], l1[1] - l2[1])

def locsum(l1: loc, l2: loc | direction) -> loc:
    return (l1[0] + l2[0], l1[1] + l2[1])

def sign(n: int) -> int:
    if n < 0:
        return -1
    elif n > 0:
        return 1
    else:
        return 0

currentside = False  # which side are we on?
currentdir: direction = direction.topleft #
inside = None

# we keep for each corner which direction it it wrapping, and which side that inside corner is
corners: dict[loc, tuple[direction, bool]] = {}
for l1, l2, l3 in zip(reds, reds[1:] + reds[:1], reds[2:] + reds[:2]):
    if l1[0] == l3[0] or l1[1] == l3[1]:
        print("oh no")  # would complicate things if not true

    # l1,l2,l3 is a 90 degree corner, l1 and l2 share 1 coordinate, l2 and l3 share the other coordinate
    # mathematically I think (l3 - l2) - (l2 - l1) is the direction of inside corner
    dir = locdiff(locdiff(l3, l2), locdiff(l2, l1))
    dir = direction(sign(dir[0]), sign(dir[1]))

    # currentside is the side of l1, do we need to flip it for l2?
    # there's two possiblities, 4x rotationally symmetric:
    # either we turn the same way as before, or we turn the opposite way
    # this means that dir (direction of l2's inside corner) plus currentdir (direction of l1's inside corner)
    # is either (0,0) -> they cancel out -> flip
    # or not -> don't flip
    dirsum = locsum(dir, currentdir)
    if dirsum == (0, 0):
        currentside = not currentside
    # from here on, currentside is the side of the inside of l2

    currentdir = dir

    if l2 == maxred:
        inside = currentside # we know whether inside is the True or False side now
    corners[l2] = (dir, currentside)

print(f"maxred at {maxred}, inside is {inside}")

bestsquares: dict[tuple[loc, loc], int] = {}
swappables = set(greens) | set(reds)

assert len(set(reds)) == len(reds)
assert set(greens) - set(reds) == set(greens)
assert len(set(greens)) == len(greens)


def squaresize(l1: tuple[int, int], l2: tuple[int, int]) -> int:
    hordist = abs(l1[0] - l2[0]) + 1
    verdist = abs(l1[1] - l2[1]) + 1
    return hordist * verdist


for i in range(len(reds) - 1):
    for j in range(i + 1, len(reds)):
        sqsize = squaresize(reds[i], reds[j])
        bestsquares[(reds[i], reds[j])] = sqsize

sortedbestsquares = sorted([(sz, locs) for (locs, sz) in bestsquares.items()])[::-1]
print(sortedbestsquares[:5])


# part 2
# outside, to start with
notswappables = (
    {(x, 0) for x in range(maxx + 1)}
    | {(x, maxy) for x in range(maxx + 1)}
    | {(0, y) for y in range(maxy + 1)}
    | {(maxx, y) for y in range(maxy + 1)}
) - swappables

def outsides(l: loc, d: direction, side: bool) -> list[loc]:
    return [
        locsum(l, dir)
        for dir in list(direction)
        if (
            (side == inside and dir != d)
            or
            (side != inside and dir == d)
        )
    ]

def isinside(l:loc, tl: loc, br: loc) -> bool:
    return tl[0] <= l[0] <= br[0] and tl[1] <= l[1] <= br[1]

for sz, locs in sortedbestsquares:

    # find the four corners
    # top left
    l1 = (min(locs[0][0], locs[1][0]), min(locs[0][1], locs[1][1]))
    # top right (do we need this one?)
    # l2 = (max(locs[0][0], locs[1][0]), min(locs[0][1], locs[1][1]))
    # bottom right
    l3 = (max(locs[0][0], locs[1][0]), max(locs[0][1], locs[1][1]))
    # bottom left (do we need this one?)
    # l4 = (min(locs[0][0], locs[1][0]), max(locs[0][1], locs[1][1]))

    maybeok = True
    # for each edge between two corners, we'll check if the "outside" edge passes through the square
    for r1, r2 in zip(reds, reds[1:] + reds[:1]):
        dir1, side1 = corners[r1]
        dir2, side2 = corners[r2]
        outr1 = locdiff(r1, dir1) if side1 == inside else locsum(r1, dir1)
        outr2 = locdiff(r2, dir2) if side2 == inside else locsum(r2, dir2)
        assert outr1[0] == outr2[0] or outr1[1] == outr2[1], (outr1, outr2)

        # check overlap with square
        if outr1[0] == outr2[0]: # vertical line, constant x
            x = outr1[0]
            if l1[0] <= x <= l3[0]:
                # overlapping x, check y range
                minyline = min(outr1[1], outr2[1])
                maxyline = max(outr1[1], outr2[1])
                if not (maxyline < l1[1] or minyline > l3[1]):
                    # overlap!
                    maybeok = False
                    break
        else: # horizontal line, constant y
            y = outr1[1]
            if l1[1] <= y <= l3[1]:
                # overlapping y, check x range
                minxline = min(outr1[0], outr2[0])
                maxxline = max(outr1[0], outr2[0])
                if not (maxxline < l1[0] or minxline > l3[0]):
                    # overlap!
                    maybeok = False
                    break

    if maybeok:

        # we're done, this works
        print(sz, locs)
        assert locs[0] in reds and locs[1] in reds
        # printgrid((set(locs), "#"), (reds, "R"), (greens, "G"))
        break

    else:

        print(
            f"found outside {outr1, outr2} inside square size {sz} at {locs}, skipping"
        )
        # printgrid((set(locs), "#"), (reds, "R"), (greens, "G"), ({outr1, outr2}, "X"))


