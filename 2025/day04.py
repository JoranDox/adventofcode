
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2025/day04inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2025/day04input.txt")) as f:
    data = f.read().strip()

orig_map: dict[tuple[int,int], int] = {}

ymax = 0
xmax = 0
for y, line in enumerate(data.splitlines()):
    for x, char in enumerate(line):
        if char == "@":
            orig_map[(x, y)] = 1
            if x > xmax:
                xmax = x
            if y > ymax:
                ymax = y

def printmap(map: dict[tuple[int,int], int]):
    for y in range(ymax + 1):
        row = ""
        for x in range(xmax + 1):
            if (x, y) in map:
                row += "@"
            else:
                row += " "
        print(row)
    print()

counter = 0
for (x,y) in orig_map:
    neighbourcounter = -1 # we're counting ourselves later
    for xdelta in (-1, 0, 1):
        for ydelta in (-1, 0, 1):
            if (x + xdelta, y + ydelta) in orig_map:
                neighbourcounter += 1
    if neighbourcounter < 4:
        counter += 1

print(counter)

# part 2:

removed = 0
current_map = orig_map.copy()
while current_map:
    known = list(current_map)
    any_removed = False
    for (x,y) in known:
        neighbourcounter = -1 # we're counting ourselves later
        for xdelta in (-1, 0, 1):
            for ydelta in (-1, 0, 1):
                if (x + xdelta, y + ydelta) in current_map:
                    neighbourcounter += 1
        if neighbourcounter < 4:
            del current_map[(x, y)]
            removed += 1
            any_removed = True
    if not any_removed:
        break
    # printmap(current_map)
print(removed)


# comprehension version part 2
current_map = orig_map.copy()
newmap = {}
while True:
    newmap = {
        (x,y):v for (x,y),v in current_map.items()
        if sum(
            1 for xdelta in (-1,0,1)
              for ydelta in (-1,0,1)
              if (x + xdelta, y + ydelta) in current_map
        ) - 1 >= 4
    }
    if len(newmap) == len(current_map):
        break
    current_map = newmap
print(len(orig_map) - len(newmap))
