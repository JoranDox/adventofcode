import numpy as np
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day13inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day13input.txt")) as f:
    data = f.read().strip()

accum = 0
accump2 = 0
for _pattern in data.split("\n\n"):
    # horizontal

    pattern = np.array([[c for c in line] for line in _pattern.splitlines()])
    print(pattern)
    maxy = len(pattern)
    maxx = len(pattern[0])
    # for y in range(1, maxy):
        
    #     print(y)
    #     print(pattern[:y])
    #     print()
    #     print(np.flipud(pattern[y:2*y]) == pattern[:y]) # TODO: cutoff front of pattern[:y]
    #     print()
    for y in range(1, maxy):
        mirror = y
        height = min(maxy - y, y)
        start = max(y-height, 0)
        end=min(maxy, y + height)
        print(y, start, mirror, end)
        p1 = pattern[start:mirror]
        print(p1)
        print()
        p2 = np.flipud(pattern[mirror:end])
        print(p2)
        print("smudgyness:", (p1 == p2).sum())
        if (p1 == p2).all():
            print("found vert at", y)
            accum += y * 100
        if (p1 == p2).sum() == (p1.shape[0] * p1.shape[1] - 1):
            print("found vert smudge at", y)
            accump2 += y * 100
        print()
    print("p1:",accum)
    print("p2:",accump2)

    for x in range(1, maxx):
        mirror = x
        width = min(maxx - x, x)
        start = max(x-width, 0)
        end=min(maxx, x + width)
        print(x, start, mirror, end)
        p1 = pattern[:,start:mirror]
        print(p1)
        print()
        p2 = np.fliplr(pattern[:,mirror:end])
        print(p2)
        print("smudgyness:", (p1 == p2).sum())
        if (p1 == p2).all():
            print("found hor at", x)
            accum += x
        if (p1 == p2).sum() == (p1.shape[0] * p1.shape[1] - 1):
            print("found hor smudge at", x)
            accump2 += x
        print()
    print("p1:",accum)
    print("p2:",accump2)
    # break

