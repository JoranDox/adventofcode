filename = "day14input.txt"
# filename = "day14inputex.txt"
# filename = "day14inputex2.txt"
with open(filename) as infile:
    inputs = [line.strip().split(" = ") for line in infile]

# part one


def applymaskval(memval, maskval):
    if maskval == "X":
        return memval
    else:
        return maskval


def applymaskrow(memrow, mask):
    return "".join(
        [applymaskval(memval, maskval) for memval, maskval in zip(memrow, mask)]
    )


# memory = {}
# mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# for op, arg in inputs:
#     if op == "mask":
#         mask = arg
#     else:
#         memory[op[4:-1]] = applymaskrow(format(int(arg), "b").zfill(36), mask)

# accum = 0
# for val in memory.values():
#     accum += int(val, 2)
# print(accum)

# part two


def applymaskdict(loc, mask, val):
    locs = [loc]
    for i, maskval in enumerate(mask):
        if maskval == "0":
            # unchanged
            pass
        elif maskval == "1":
            # overwrite 1
            locs = ["".join([*(loc[:i]), "1", *(loc[i + 1 :])]) for loc in locs]
        elif maskval == "X":
            # floating
            templocs = []
            for loc in locs:
                templocs.append("".join([*(loc[:i]), "0", *(loc[i + 1 :])]))
                templocs.append("".join([*(loc[:i]), "1", *(loc[i + 1 :])]))
            locs = templocs
        else:
            assert False

    return {k: val for k in locs}


memory = {}
mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
import json

for op, arg in inputs:
    json.dumps(memory, indent=4)
    if op == "mask":
        # print(f"{mask=}")
        mask = arg
    else:
        # print(f"{op=}, {arg=}")
        memory.update(
            applymaskdict(
                format(int(op[4:-1]), "b").zfill(36),
                mask,
                format(int(arg), "b").zfill(36),
            )
        )

accum = 0
for val in memory.values():
    accum += int(val, 2)
print(accum)
