import collections
import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day10inputtest2.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day10input.txt")) as f:
    data = f.read().strip()

locations = []
for y, line in enumerate(data.splitlines()):
    locations.append([char for char in line])
    if "S" in line:
        sy = y
        sx = line.find("S")

# print(locations)
maxy = len(data.splitlines())
maxx = len(data.splitlines()[0])


def neighbours(x, y):
    match locations[y][x]:
        case "|":
            # | is a vertical pipe connecting north and south.
            return (x, y + 1), (x, y - 1)
        case "-":
            # - is a horizontal pipe connecting east and west.
            return (x + 1, y), (x - 1, y)
        case "L":
            # L is a 90-degree bend connecting north and east.
            return (x, y - 1), (x + 1, y)
        case "J":
            # J is a 90-degree bend connecting north and west.
            return (x, y - 1), (x - 1, y)
        case "7":
            # 7 is a 90-degree bend connecting south and west.
            return (x, y + 1), (x - 1, y)
        case "F":
            # F is a 90-degree bend connecting south and east.
            return (x, y + 1), (x + 1, y)
        case ".":
            # . is ground; there is no pipe in this tile.
            print("huh")
            return ()
        case "S":
            # unknown, return everything
            return (
                (x - 1, y),
                (x, y - 1),
                (x, y + 1),
                (x + 1, y),
            )


path = {(sx, sy): 0}
tocheck = collections.deque()
for nx, ny in neighbours(sx, sy):
    # print((nx, ny), locations[ny][nx])
    if (sx, sy) in neighbours(nx, ny):
        # print("actual neighbour")
        tocheck.append(((nx, ny), 1))
# print("S", sx, sy)

actualneighs = set(loc for loc, _ in tocheck)
for shape in "|-LJ7F":
    locations[sy][sx] = shape
    # print(shape, actualneighs, set(neighbours(sx, sy)))
    if actualneighs == set(neighbours(sx, sy)):
        # print(f"actual neighbours found, S replaced with {shape}")
        break

# exit()
# print(tocheck)
while tocheck:
    (cx, cy), dist = tocheck.popleft()
    for neigh in neighbours(cx, cy):
        if neigh in path:
            if dist + 1 < path[neigh]:
                print("huh2")
                path[neigh] = dist + 1
                tocheck.append((neigh, dist + 1))
            # else: exit condition
        else:
            path[neigh] = dist + 1
            tocheck.append((neigh, dist + 1))

# print(path)
print("p1:", dist)


def flood(x, y):
    start = set()
    consequent = {(x, y)}
    while start != consequent:
        start = consequent

        consequent = set()
        for cx, cy in start:
            consequent |= {
                (fx, fy)
                for fx, fy in (
                    (cx, cy - 1),
                    (cx - 1, cy),
                    (cx, cy),
                    (cx + 1, cy),
                    (cx, cy + 1),
                )
                if (
                    (fx, fy) not in path
                    and (fx, fy) not in consequent
                    and fx >= 0
                    and fy >= 0
                    and fx <= maxx
                    and fy <= maxy
                )
            }
            # print(consequent)
    return consequent


def highlight(given):
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if (x, y) in given:
                print("*", end="")
            elif (x, y) in path:
                print(char, end="")
            else:
                print(".", end="")
        print()


# exit()
areas = [frozenset(path)]
maybe_interiorareas = []
accum = 0
# print(areas)
for y in range(maxy):
    state = "mid", False
    for x in range(maxx):
        if (x, y) in path:
            match (locations[y][x], state):
                case "L", (s, b):
                    assert s == "mid"
                    state = "top", not b
                case "J", ("top", b):
                    state = "mid", not b
                case "J", ("bot", b):
                    state = "mid", b
                case "F", (s, b):
                    assert s == "mid"
                    state = "bot", not b
                case "7", ("bot", b):
                    state = "mid", not b
                case "7", ("top", b):
                    state = "mid", b
                case "|", (s, b):
                    assert s == "mid"
                    state = "mid", not b
                case "-", (s, b):
                    assert s != "mid"
                    pass  # nothing changes
                case _:
                    assert (
                        False
                    ), f"something went wrong at {x,y}, {path.get((x,y))}, {state}"

        if not (any((x, y) in area for area in areas)):
            areas.append(f := flood(x, y))
            # print(f)

            if state[1]:
                # highlight(f)
                accum += len(f)
# print()
# highlight(path)
print("p2:", accum)
