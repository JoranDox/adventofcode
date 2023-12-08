import string

import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day03inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day03input.txt")) as f:
    data = f.read().strip()

# print(string.ascii_letters)


def prio(item):
    return string.ascii_letters.index(item) + 1


# print(prio("a"))
# print(prio("z"))
# print(prio("A"))
# print(prio("Z"))

# part 1
accum = 0
for line in data.splitlines():
    # print(len(line), len(line)//2)
    # print(line)
    # print(line[:len(line)//2])
    # print(line[len(line)//2:])
    intersect = set(line[: len(line) // 2]) & set(line[len(line) // 2 :])
    assert len(intersect) == 1
    # print(intersect)
    # print(prio(list(intersect)[0]))
    accum += prio(list(intersect)[0])
print("p1:", accum)

accum2 = 0
splitted = data.splitlines()
while splitted:
    curr3, splitted = splitted[:3], splitted[3:]
    intersect = set(curr3[0]) & set(curr3[1]) & set(curr3[2])
    # print(intersect)
    accum2 += prio(list(intersect)[0])
print("p2:", accum2)
