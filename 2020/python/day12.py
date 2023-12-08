filename = "day12inputex.txt"
filename = "day12input.txt"


with open(filename) as infile:
    instructions = [(line[0], int(line[1:])) for line in infile]

north = (0, -1)
east = (1, 0)
south = (0, 1)
west = (-1, 0)
currentfacing = east
location = (0, 0)

order = north, east, south, west
translation = {
    "N": north,
    "S": south,
    "E": east,
    "W": west,
}


def add(loc, dist, multiplier=1):
    (lx, ly), (dx, dy) = loc, dist
    return lx + dx * multiplier, ly + dy * multiplier


# #part1
for direction, distance in instructions:
    # print(direction, distance, location, currentfacing)
    if direction in "NSEWF":
        # does not change facing somehow
        location = add(location, translation.get(direction, currentfacing), distance)
    elif direction == "R":
        assert not distance % 90, f"{distance=}"
        currentindex = order.index(currentfacing)
        steps = distance // 90
        # print(currentindex, steps)
        currentfacing = order[
            (order.index(currentfacing) + (distance // 90)) % len(order)
        ]
    elif direction == "L":
        assert not distance % 90, f"{distance=}"
        currentindex = order.index(currentfacing)
        steps = distance // 90
        # print(currentindex, steps)
        currentfacing = order[
            (order.index(currentfacing) - (distance // 90)) % len(order)
        ]
    else:
        print("fuck")
    # print(location, currentfacing)
x, y = location
print(abs(x) + abs(y))

# part 2
print("part 2")


def rotateleft(loc, steps=1):
    lx, ly = loc
    while steps:
        steps -= 1
        lx, ly = ly, -lx
    return lx, ly


def rotateright(loc, steps=1):
    lx, ly = loc
    while steps:
        steps -= 1
        lx, ly = -ly, lx
    return lx, ly


location = (0, 0)
waypoint = add(north, east, 10)
for direction, distance in instructions:
    # print("  ", location, waypoint)
    # print(direction, distance)
    if direction == "F":
        location = add(location, waypoint, distance)
    elif direction in "NSEW":
        # does not change facing somehow
        waypoint = add(waypoint, translation[direction], distance)
    elif direction == "R":
        steps = distance // 90

        waypoint = rotateright(waypoint, steps)

    elif direction == "L":
        steps = distance // 90

        waypoint = rotateleft(waypoint, steps)
    else:
        print("fuck")

# print("  ", location, waypoint)

x, y = location
print(abs(x) + abs(y))
