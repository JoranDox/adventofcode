
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
#with open(aoc_dir.joinpath("input/2022/day04inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day04input.txt")) as f:
    data = f.read().strip()

counter = 0
counter2 = 0
for line in data.splitlines():
#for line in data.split("\n\n"):
    a,b = line.split(",")
    a_start, a_stop = [int(k) for k in a.split("-")]
    b_start, b_stop = [int(k) for k in b.split("-")]
    aset = set(range(a_start, a_stop + 1))
    bset = set(range(b_start, b_stop + 1))
    # print(aset, bset)
    if aset >= bset or bset >= aset:
        counter += 1

    if aset & bset:
        counter2 += 1
print(counter)
print(counter2)

