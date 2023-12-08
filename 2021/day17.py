with open("day17inputtest.txt") as f:
    # with open("day17input.txt") as f:
    data = f.read().strip()

# for line in data.splitlines():

target = {"x": (235, 259), "y": (-118, -62)}

# target = {
#     "x":(20,30),
#     "y":(-10,-5)
# }

loc = 0, 0


def stepl(loc, velocity):
    return (loc[0] + velocity[0]), (loc[1] + velocity[1])


def stepv(velocity):
    v0 = velocity[0]
    if v0 > 0:
        v0 -= 1
    if v0 < 0:
        v0 += 1
    velocity = v0, (velocity[1] - 1)
    return velocity


def step(loc, velocity):
    return stepl(loc, velocity), stepv(velocity)


xmin, xmax = target["x"]
ymin, ymax = target["y"]

velocity = (6, 9)
loc = (0, 0)
for i in range(20):
    loc, velocity = step(loc, velocity)
    # print(loc,velocity)

validxs = set()
for x in range(1, 1000):
    steps = 0
    velocity = (x, 0)
    loc = (0, 0)
    # print("checking", x)
    while loc[0] < xmax:
        steps += 1
        loc, velocity = step(loc, velocity)
        print(loc, velocity)
        if xmin <= loc[0] <= xmax:
            validxs |= {(x, steps)}
            print("found", x, steps)
            break
        if velocity[0] == 0:
            break
# minimal steps
print(validxs)


bestx = 0
maxy = 0
corrects = set()
for x, minsteps in validxs:
    # print("checking y", y)
    # y = ymin
    curmaxy = 0
    for y in range(ymin, -ymin):
        # while True:
        # y += 1
        velocity = (x, y)
        loc = (0, 0)
        # print("checking", velocity)
        for i in range(minsteps):
            loc, velocity = step(loc, velocity)
            curmaxy = max(curmaxy, loc[1])

        for moresteps in range(500):
            if (xmin <= loc[0] <= xmax) and (ymin <= loc[1] <= ymax):
                print("checked x", x, "with", steps, "steps, starting v = ", (x, y))
                print("final loc", loc, "final v", velocity)
                corrects |= {(x, y)}
                if curmaxy > maxy:
                    print(
                        f"({xmin=} <= {loc[0]} <= {xmax=}) and ({ymin=} <= {loc[1]} <= {ymax})"
                    )
                    maxy = curmaxy
                    bestx = x
                    print("found a better y", y)

            loc, velocity = step(loc, velocity)
            curmaxy = max(curmaxy, loc[1])

        # if loc[1] > ymax:
        #     # print("stop")
        #     break

print(bestx, maxy)
print(corrects, len(corrects))
