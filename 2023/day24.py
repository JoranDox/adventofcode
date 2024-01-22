
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
with open(aoc_dir.joinpath("input/2023/day24inputtest.txt")) as f:
# with open(aoc_dir.joinpath("input/2023/day24input.txt")) as f:
    data = f.read().strip()

for line in data.splitlines():
#for line in data.split("\n\n"):


