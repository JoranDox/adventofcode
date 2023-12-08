import string
import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day01inputtest.txt")) as f:
# with open(aoc_dir.joinpath("input/2023/day01inputtest2.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day01input.txt")) as f:
    data = f.read().strip()

accum = 0
# for line in data.splitlines():
# #for line in data.split("\n\n"):
#     l = [i for i in line if i in string.digits]
#     print(l[0], l[-1])
#     newint = int(f"{l[0]}{l[-1]}")
#     accum += newint
#     print(accum)

# part two

accum = 0
for line in data.splitlines():
    # print(line)
    firstnum = None
    firstnumstr = None
    firstnumindex = None
    lastnum = None
    lastnumstr = None
    lastnumindex = None
    for numstr, num in [
        ("one", 1),
        ("two", 2),
        ("three", 3),
        ("four", 4),
        ("five", 5),
        ("six", 6),
        ("seven", 7),
        ("eight", 8),
        ("nine", 9),
        *zip(string.digits, string.digits),
    ]:
        index = line.find(numstr)
        if index >= 0:
            print(numstr, index)
            if firstnumindex is None or index < firstnumindex:
                # print(f"f: found {index} for {numstr}")
                firstnum = num
                firstnumstr = numstr
                firstnumindex = index
        index = line.rfind(numstr)
        if index >= 0:
            if lastnumindex is None or index > lastnumindex:
                # print(f"l: found {index} for {numstr}")
                lastnum = num
                lastnumstr = numstr
                lastnumindex = index
    i = int(f"{firstnum}{lastnum}")
    print(i, firstnumstr, lastnumstr, line)
    accum += i
    print(accum)
print(accum)
# tried: 54110
