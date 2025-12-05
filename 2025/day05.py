
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2025/day05inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2025/day05input.txt")) as f:
    data = f.read().strip()

# for line in data.splitlines():
fresh_ranges, available_ingredients = data.split("\n\n")

fresh: list[range] = []
for line in fresh_ranges.splitlines():
    start, end = line.split("-")
    fresh.append(range(int(start), int(end)+1))

counter = 0
for ingredient in available_ingredients.splitlines():
    ingredient_id = int(ingredient)
    if any(ingredient_id in r for r in fresh):
        # print(f"{ingredient_id} is fresh")
        counter += 1
print(counter)

# part 2

# note these ranges are inclusive of the end value
def rangeoverlap(r1: tuple[int,int], r2: tuple[int,int]) -> tuple[int,int] | None:
    r1start = r1[0]
    r2start = r2[0]
    if r1start > r2start:
        return rangeoverlap(r2, r1)
    r1end = r1[1]
    r2end = r2[1]

    # return options:
    # initial range unchanged -> only when no overlap
    # absorbed in current range -> any other case

    # now we have certainty that r1start <= r2start
    # so the options are:
    if r1start == r2start:
        # just return the longest one
        return (r1start, max(r1end, r2end))
    # else, we're certain r1start < r2start
    # this leaves us with options:
    if r1end < r2start:
        # return None, no overlap, let the caller handle it
        return None
    if r1end >= r2start:
        # includes perfect merge where r1end == r2end
        return (r1start, max(r1end, r2end))
    print("unhandled case?", r1, r2)
    assert False

merged: list[tuple[int,int]] = []
for line in fresh_ranges.splitlines():
    start, end = line.split("-")
    r = (int(start), int(end))
    newmerged: list[tuple[int,int]] = []
    for m in merged:
        overlap = rangeoverlap(m, r)
        if not overlap:
            # no overlap, just append m and continue
            newmerged.append(m)
        else:
            # merged
            r = overlap

    newmerged.append(r)
    merged = newmerged

counter2 = 0
for start,end in merged:
    counter2 += end - start + 1
print(counter2)
