import re

import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
with open(aoc_dir.joinpath("input/2025/day02inputtest.txt")) as f:
# with open(aoc_dir.joinpath("input/2025/day02input.txt")) as f:
    data = f.read().strip()

counter = 0
summer = 0
part2summer = 0
# for line in data.splitlines():
# for line in data.split(","):
#     start, end = line.strip().split("-", 2)

#     start = int(start)
#     end = int(end)
#     for n in range(start, end + 1):
#         s = str(n)
#         l = len(s)
#         if s[:l//2] == s[l//2:]:
#             counter += 1
#             summer += n
#             print(n, "is doubled", f"count={counter}", f"sum={summer}")

print("part2")

for line in data.split(","):
    start, end = line.strip().split("-", 2)
    start = int(start)
    end = int(end)
    for n in range(start, end + 1):
        s = str(n)
        if re.match(r"^(.*)\1+$", s):
            part2summer += n
            print(n, "is multiple", f"part2sum={part2summer}")