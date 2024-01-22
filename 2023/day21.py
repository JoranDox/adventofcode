
import pathlib
import collections
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day21inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day21input.txt")) as f:
    data = f.read().strip()

even_locs = set()
odd_locs = set()
unchecked = set()
locs = {}
for y, line in enumerate(data.splitlines()):
    for x, char in enumerate(line):
        locs[(x,y)] = char
        if char == "S":
            even_locs.add((x,y))
            unchecked.add((x,y))



def neighbours(x,y):
    return {
        (nx,ny) for nx,ny in
        (
            (x-1,y),
            (x+1,y),
            (x,y-1),
            (x,y+1),
        )
        if locs[(nx,ny)] != "#"
    }

steps = 64
newunchecked = collections.deque()
for step in range(steps):

    unchecked = {
        s
        for x,y in unchecked
        for s in neighbours(x,y)
    }
    print(unchecked, len(unchecked))

    # if step % 2:
    #     # something
    #     even_locs