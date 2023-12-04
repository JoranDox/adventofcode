from collections import defaultdict
import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
with open(aoc_dir.joinpath("input/2023/day04inputtest.txt")) as f:
# with open(aoc_dir.joinpath("input/2023/day04input.txt")) as f:
    data = f.read().strip()

accump1 = 0
scratchcards_got: dict[int,int] = defaultdict(int)
for line in data.splitlines():
    game, info = line.split(":")
    winning, owned = info.split("|")
    gamenr = int(game.split()[1])
    scratchcards_got[gamenr] += 1
    winningnrs = {int(w) for w in winning.split()}
    ownnrs = {int(o) for o in owned.split()}
    overlap = winningnrs & ownnrs
    if overlap:
        cardworth = 2 ** (len(overlap) - 1)
        for i in range(len(overlap)):
            scratchcards_got[gamenr + i + 1] += scratchcards_got[gamenr]
    else:
        cardworth = 0
    # print("game", gamenr, len(overlap), cardworth)
    accump1 += cardworth
    # print("accump1", accump1)
print("p1:", accump1)
# print(scratchcards_got)
print("p2:", sum(scratchcards_got.values()))
