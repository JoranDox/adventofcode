import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2025/day07inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2025/day07input.txt")) as f:
    data = f.read().strip()

grid: dict[tuple[int,int], str] = {}
start = None
maxy = 0
maxx = 0
for y, line in enumerate(data.splitlines()):
    for x, char in enumerate(line):
        if char == "^":
            grid[(x, y)] = char
        if char == "S":
            start = (x, y)
        maxx = max(maxx, x)
    maxy = y

assert start is not None

def printline(beams: set[tuple[int,int]], grid: dict[tuple[int,int], str], y: int):
    accum: list[str] = []
    for x in range(maxx + 1):
        if (x, y) in beams:
            accum.append("|")
        elif (x, y) in grid:
            accum.append("^")
        else:
            accum.append(".")
    print("".join(accum))

beams = {start}
counter = 0
for y in range(maxy+1):
    # printline(beams, grid, y)
    printline(beams, grid, y)
    samebeams = {
        (x, y + 1)
        for (x, _) in beams
        if (x, y + 1) not in grid
    }
    rightsplit = {
        (x + 1, y + 1)
        for (x, _) in beams
        if (x, y + 1) in grid
    }
    leftsplit = {
        (x - 1, y + 1)
        for (x, _) in beams
        if (x, y + 1) in grid
    }
    beams = samebeams | rightsplit | leftsplit
    counter += len(rightsplit)
    # print(sorted(beams))



print(beams, len(beams))
print(counter)

# part 2


beams = {start[0]: 1}
counter = 0
for y in range(maxy+1):
    samebeams = {
        x: count
        for (x, count) in beams.items()
        if (x, y + 1) not in grid
    }
    rightsplit = {
        x + 1: count
        for (x, count) in beams.items()
        if (x, y + 1) in grid
    }
    leftsplit = {
        x - 1: count
        for (x, count) in beams.items()
        if (x, y + 1) in grid
    }

    beams = {
        x: (samebeams.get(x, 0) + rightsplit.get(x, 0) + leftsplit.get(x, 0))
        for x in samebeams | rightsplit | leftsplit # naive join
    }
print(beams)
print(sum(beams.values()))