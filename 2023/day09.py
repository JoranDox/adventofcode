import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day09inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day09input.txt")) as f:
    data = f.read().strip()


def extrapolate(xs):
    diffs = [x2 - x1 for x1, x2 in zip(xs[:-1], xs[1:])]
    # print("diffs", diffs)
    if any(diffs):
        ext = extrapolate(diffs) + diffs[-1]
        print("diffs", diffs, ext)
        return ext
    else:
        print("diffs", diffs, 0)
        return 0


def extrapolatebackwards(xs):
    diffs = [x2 - x1 for x1, x2 in zip(xs[:-1], xs[1:])]
    print(diffs)
    if any(diffs):
        ext = diffs[0]- extrapolatebackwards(diffs)
        print("diffs", ext, diffs)
        return ext
    else:
        print("diffs", 0, diffs)
        return 0


accum = 0
accum2 = 0
for line in data.splitlines():
    # print(line)
    line_int = [int(x) for x in line.split()]
    print(line_int)
    print("forwards")
    p = extrapolate(line_int) + line_int[-1]
    print("diffs", line_int, p)
    print("back")
    p2 = line_int[0] - extrapolatebackwards(line_int) 
    print("diffs", p2, line_int)
    accum += p
    accum2 += p2
print(accum)
print(accum2)
# for line in data.split("\n\n"):
