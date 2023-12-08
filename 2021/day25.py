from typing import Counter
import numpy as np
import copy

# with open("day25inputtest.txt") as f:
with open("day25input.txt") as f:
    data = f.read().strip()

world = tuple(tuple(line.strip()) for line in data.splitlines())

npworld = np.array(world)

print(npworld)


def tsummod(a, b, dimmaxxes):
    return tuple(((x + y) % d) for x, y, d in zip(a, b, dimmaxxes))


def testeq(a, b):
    assert a == b, f"{a} is not {b}"


testeq(tsummod((1, 0), (0, 1), (2, 2)), (1, 1))
testeq(tsummod((3, 3), (0, 1), (2, 2)), (1, 0))
xmax = len(world[0])
ymax = len(world)
print(xmax, ymax)

dirmap = {
    ">": (1, 0),
    "v": (0, 1),
    (1, 0): ">",
    (0, 1): "v",
}


def worldprint(world):
    for line in world:
        print("".join(line))


def countworld(world):
    c = Counter()
    for line in world:
        c.update(line)
    return c["."]


def step(world, direction=(1, 0)):
    c = countworld(world)
    npworld = np.array(world)
    npworld2 = np.array(world)
    for y in range(ymax):
        for x in range(xmax):  # assume the world is rectangular
            newloc = tsummod((x, y), direction, (xmax, ymax))
            if npworld.T[(x, y)] == dirmap[direction]:
                # print("considering", (x,y))
                # print("correct direction", dirmap[direction])
                if npworld.T[newloc] == ".":
                    # print("empty spot at", newloc)
                    # print(f"moving {dirmap[direction]} from {(x,y)} to {newloc}")
                    # move
                    npworld2.T[x, y] = "."
                    npworld2.T[newloc] = dirmap[direction]
                else:
                    # print("no empty spot at", newloc, ", has", npworld.T[newloc])
                    pass
    assert c == countworld(npworld2), (c, countworld(npworld2))
    return tuple(tuple(line) for line in npworld2)


changed = True
prevworld = copy.deepcopy(world)
steps = 0
while changed:
    # worldprint(world)
    # print()
    steps += 1
    world = step(
        world,
        (1, 0),
    )
    # worldprint(world)
    world = step(
        world,
        (0, 1),
    )
    changed = world != prevworld
    prevworld = copy.deepcopy(world)
    print(steps)
    # if steps >= 1:
    #     break
worldprint(world)
print(steps)
