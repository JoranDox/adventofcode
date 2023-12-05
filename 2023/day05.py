
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day05inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day05input.txt")) as f:
    data = f.read().strip()

def mapping(outputs, inputs, ranges, number):
    inputs = [int(i) for i in inputs]
    outputs = [int(i) for i in outputs]
    ranges = [int(i) for i in ranges]
    number = int(number)
    for i,o,r in zip(inputs,outputs,ranges):
        if i <= number < i+r:
            # print(f"in range: {i=}, {i+r=}, {r=}, {o=}, {number=}, returning: {number - i + o}")
            return number - i + o
        # else:
            # print(f"not in range: {i=}, {i+r=}, {r=}, {number=}")
    # print(f"not in any range, just returning {number}")
    return number

def range_overlaps(r1, r2):
    # print(f"range_overlaps: {r1=}, {r2=}")
    # ranges are (start, end), not (start, length)

    overlapping_part = (
        max(r1[0],r2[0]),
        min(r1[1],r2[1])
    )
    # print(f"overlapping_part for {r1}, {r2}: {overlapping_part=}")

    if overlapping_part[0] > overlapping_part[1]:
        # no overlap
        return (
            None,
            None
        )
    else:
        endpoints = sorted([*r1, *r2])
        # print(endpoints)
        not_overlapping_parts = []
        if endpoints[0] != endpoints[1]:
            not_overlapping_parts.append((endpoints[0], endpoints[1] - 1))
        if endpoints[-2] != endpoints[-1]:
            not_overlapping_parts.append((endpoints[-2] + 1, endpoints[-1]))
        # print(overlapping_part, not_overlapping_parts)
        return (
            # overlapping
            overlapping_part,
            # not overlapping
            not_overlapping_parts
        )


# print(range_overlaps((1,5),(3,8)))
# print(range_overlaps((1,5),(3,5)))
# print(range_overlaps((0,15),(14,14)))
# print(range_overlaps((0,0),(14,14)))
# print(range_overlaps((0,13),(13,13)))

# exit()
def range_mapping(outputs, inputs, ranges, number_range):
    # print(f"range_mapping: {outputs=}, {inputs=}, {ranges=}, {number_range=}")
    returns = []
    todo = [number_range]
    for i,o,r in zip(inputs,outputs,ranges):
        # print(f"checking {i=},{o=},{r=}")
        for _range in todo:
            overlap, non_overlaps = range_overlaps((i, i+r-1), _range)
            if overlap:
                # print(f"{overlap=}, {non_overlaps=}")
                returns.append((overlap[0] - i + o, overlap[1] - i + o))
                todo.remove(_range)
                for to_check in non_overlaps:
                    right_overlap, right_non_overlaps = range_overlaps(to_check, _range)
                    if right_overlap:
                        todo.append(right_overlap)
                # print(f"range_mapping iteration: {todo=}, {returns=}")

    # print("returns", returns)
    # print("todo", todo)
    return returns + todo


for page in data.split("\n\n"):
    if page.startswith("seeds:"):
        on_hand = page.split()[1:]
        # print(f"starting with: {on_hand}")
    else:
        pagesplit = page.splitlines()
        # print(pagesplit[0])
        outputs, inputs, ranges = zip(*[p.split() for p in pagesplit[1:]])
        # print("outputs",outputs)
        # print("inputs",inputs)
        # print("ranges",ranges)
        on_hand = [
            mapping(outputs, inputs,ranges,n) for n in on_hand
        ]
        # print("on_hand:", on_hand)
        # for line in
        #     if line.endswith(":"):
        #     else:
        #         mapping =
print("p1:", min(on_hand))

# part 2
for page in data.split("\n\n"):
    if page.startswith("seeds:"):
        on_hand = [int(i) for i in page.split()[1:]]
        # print(f"starting with: {on_hand}")
        on_hand_ranges = []
        for i in range(0, len(on_hand), 2):
            on_hand_ranges.append((int(on_hand[i]), int(on_hand[i]) + int(on_hand[i+1]-1)))
        # print(f"starting with: {on_hand_ranges}")

    else:
        pagesplit = page.splitlines()
        # print(pagesplit[0])
        outputs, inputs, ranges = zip(*[p.split() for p in pagesplit[1:]])
        outputs = [int(i) for i in outputs]
        inputs = [int(i) for i in inputs]
        ranges = [int(i) for i in ranges]
        # print("outputs",outputs[:10])
        # print("inputs",inputs[:10])
        # print("ranges",ranges[:10])
        on_hand_ranges_new = []
        for _range in on_hand_ranges:
            on_hand_ranges_new.extend(range_mapping(outputs, inputs, ranges, _range))
        on_hand_ranges = on_hand_ranges_new
        # print("on_hand_ranges:", on_hand_ranges[:10])
        # for line in
        #     if line.endswith(":"):
        #     else:
        #         mapping =
        # exit()

print("p2:", min([i[0] for i in on_hand_ranges]))
