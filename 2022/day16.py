import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day16inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day16input.txt")) as f:
    data = f.read().strip()

flowrates = {}
connections = {}
for line in data.splitlines():
    fr, conns = line.split("; ")
    _, vname, _, _, rate = fr.split()
    flowrates[vname] = int(rate.split("=")[1])

    connections[vname] = [c.replace(",", "").strip() for c in conns.split()[4:]]

# print(flowrates)
# print(connections)


def shortest(start, end, max=30):
    paths = [(start,)]
    newpaths = []
    while True:
        for p in paths:
            for conn in connections[p[-1]]:
                if conn == end:
                    return len(p)
                if len(p) > max:
                    return 50
                if conn not in p:
                    newpaths.append(p + (conn,))
        # print(newpaths)
        paths = newpaths


distancematrix = {
    v1: {v2: shortest(v1, v2) for v2 in connections if ((v2 != v1) and flowrates[v2])}
    for v1 in connections
}

# print(distancematrix)

minutes = 30
pqueue = {i: list() for i in range(minutes)}
pqueue[0].append(
    # starting path
    (0, 0, 0, "AA", tuple(), (("start", "AA"),))
)

# print(pqueue)

finished = []
partials = {}

for i in range(minutes):
    # print(i, len(pqueue[i]))
    # for p in (sorted(pqueue[i])[:-4:-1]):
    # print(p)
    for expectedflow, fr, totalflow, position, openvalves, actions in pqueue[i]:
        # open
        # if len(openvalves) == goodvalves:
        # print("maybe done")
        # finished.append((expectedflow, fr, totalflow, position, openvalves, actions))
        # print(finished[-1])

        moved = False
        for move, distance in distancematrix[position].items():
            if move not in openvalves:
                extraflow = flowrates[move] * ((minutes - i) - distance - 1)
                if i + distance + 1 < minutes and extraflow > 0:
                    moved = True
                    pqueue[i + distance + 1].append(
                        (
                            expectedflow + extraflow,
                            fr + flowrates[move],
                            totalflow + (fr * (distance + 1)),
                            move,
                            openvalves + (move,),
                            actions
                            + (
                                ("m", distance, move),
                                ("o", move),
                            ),
                        )
                    )
        if not moved:
            finished.append(
                (expectedflow, fr, totalflow, position, openvalves, actions)
            )

        if i <= 26:
            discount = sum(flowrates[valve] for valve in openvalves) * 4
            valvestocheck = frozenset(openvalves)
            partials[valvestocheck] = max(
                expectedflow - discount, partials.get(valvestocheck, 0)
            )

# for key,value in partials.items():
#     print(key, value)

# print(len(partials))
# DD, BB, JJ, HH, EE, CC
# for i in sorted(finished)[-1:]:
#     print(i)
print("p1:", sorted(finished)[-1][0])

# part 2

# you = JJ, BB, CC
# ele = DD, HH, EE
# for i in range(30):
#     p = partials.get((frozenset(("JJ", "BB", "CC")), i))
#     if p:
#         print(i, ("JJ", "BB", "CC"), p)
# for i in range(30):
#     p = partials.get((frozenset(("DD", "HH", "EE")), i))
#     if p:
#         print(i, ("DD", "HH", "EE"), p)

maxval = 0
maxvalves = None
for valves1, value1 in partials.items():
    for valves2, value2 in partials.items():
        if valves1 & valves2:
            # overlap is waste
            continue
        else:
            if maxval < value1 + value2:
                maxval = value1 + value2
                maxvalves = (valves1, valves2)

# discount1 = sum(flowrates[valve] for valve in maxvalves[0]) * 4
# discount2 = sum(flowrates[valve] for valve in maxvalves[1]) * 4
# print(maxval, maxvalves)
print("p2:", maxval)
