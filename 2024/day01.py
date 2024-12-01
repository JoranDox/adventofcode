# just for fun, visualize the points as x,y coords
import pathlib
import time
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
print(aoc_dir)
# with open(aoc_dir.joinpath("input/2024/day01inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2024/day01input.txt")) as f:
    data = f.read().strip()
print(data)
xs = []
ys = []
for line in data.splitlines():

    x, y = line.split()
    x = int(x)//1000
    y = int(y)//1000
    xs.append(x)
    ys.append(y)
print(xs, ys)
minx = min(xs)
miny = min(ys)
maxx = max(xs)
maxy = max(ys)
print(minx, maxx, miny, maxy)
time.sleep(1)
locs = {
    (x, y)
    for x, y in zip(xs, ys)
}
for y in range(miny, maxy + 1):
    line = [
        "#" if (x, y) in locs else " "
        for x in range(minx, maxx + 1)
    ]
    print("".join(line) + "|")
