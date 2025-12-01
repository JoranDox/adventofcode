
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2025/day01inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2025/day01input.txt")) as f:
    data = f.read().strip()

dial = 50
zerocount = 0
method0x434C49434Bcount = 0

for line in data.splitlines():
    predial = dial
    premethod0x434C49434Bcount = method0x434C49434Bcount
    match line[0], int(line[1:]), dial:
        case "R", n, 100:
            dial = n
        case "R", n, _:
            dial += n
        case "L", n, 0:
            dial = 100 - n
        case "L", n, _:
            dial -= n
        case _:
            raise ValueError("unreachable")
    while dial > 100:
        method0x434C49434Bcount += 1
        dial -= 100
        print(">100")
    while dial < 0:
        method0x434C49434Bcount += 1
        dial += 100
        print("<0")
    if dial == 100 or dial == 0:
        method0x434C49434Bcount += 1
        zerocount += 1
    print(predial, line, dial, zerocount, method0x434C49434Bcount, method0x434C49434Bcount - premethod0x434C49434Bcount)

# 6352 too low
# 6358
# 6364 too high


