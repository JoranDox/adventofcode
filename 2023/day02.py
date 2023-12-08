import functools
import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day02inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day02input.txt")) as f:
    data = f.read().strip()

accum = 0
accumpower = 0
colourmap = {
    "red": 12,
    "green": 13,
    "blue": 14,
}
for game in data.splitlines():
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    gameid, runs = game.split(":")
    gameid_num = int(gameid[4:])
    ok = True
    mincubes = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }
    for run in runs.split(";"):
        draws = run.split(",")
        for draw in draws:
            num, colour = draw.split()
            # part 1
            if int(num) > colourmap[colour]:
                # 12 red cubes, 13 green cubes, and 14 blue cubes
                # print(f"{gameid} is impossible because of {num}, {colour}")
                ok = False
            # part 2
            if int(num) > mincubes[colour]:
                mincubes[colour] = int(num)

    # part 1
    if ok:
        # print(f"{gameid} is ok")
        accum += gameid_num
        # print(accum)
    # part 2:
    power = functools.reduce(lambda x, y: x * y, mincubes.values())
    accumpower += power

print(accum)
print(accumpower)
