import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day01inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day01input.txt")) as f:
    data = f.read().strip()

elves = []
for elfdata in data.split("\n\n"):
    elves.append([])
    for calories in elfdata.splitlines():
        elves[-1].append(int(calories))
print(elves)


# part 1
print(max([sum(x) for x in elves]))


print(sum(sorted([sum(x) for x in elves])[-3:]))
