
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day08inputtest.txt")) as f:
# with open(aoc_dir.joinpath("input/2023/day08inputtest2.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day08input.txt")) as f:
    data = f.read().strip()

network = {}
instructions, networkdata = data.split("\n\n")
for line in networkdata.splitlines():
    source, left, right = line.replace("=", "").replace("(", "").replace(")","").replace(",","").split()

    network[source] = (left, right)

# print(network)

currentstate = "AAA"
steps = 0
found = False
while not found:
    for letter in instructions:
        steps += 1
        if letter == "L":
            currentstate = network[currentstate][0]
        elif letter == "R":
            currentstate = network[currentstate][1]
        else:
            print("wtf")
        # print(currentstate)
        if currentstate == "ZZZ":
            print("p1:", steps)
            found = True
            break

# part 2

currentstates = [state for state in network if state.endswith("A")]
# print(sorted(currentstates))

def testloops(state):
    steps = 0
    maybe_steps = None
    while True:
        for letter in instructions:
            steps += 1
            if letter == "L":
                state = network[state][0]
                # currentstates = [network[state][0] for state in currentstates]
            elif letter == "R":
                state = network[state][1]
                # currentstates = [network[state][1] for state in currentstates]
            if state.endswith("Z"):
                if maybe_steps:
                    # second time we get here
                    print(steps, maybe_steps, steps / maybe_steps)
                    return maybe_steps
                else:
                    maybe_steps = steps

finalstates = [state, testloops(state) for state in currentstates]


# steps = 0
# found = False
# finalstates = []
# while not found:
#     for letter in instructions:
#         steps += 1
#         if letter == "L":
#             currentstates = [network[state][0] for state in currentstates]
#         elif letter == "R":
#             currentstates = [network[state][1] for state in currentstates]
#         else:
#             print("wtf")

#         for state in currentstates:
#             if state.endswith("Z"):
#                 finalstates.append((state,steps))
#         currentstates = [state for state in currentstates if not state.endswith("Z")]

#         # print(currentstates)
#         if not currentstates:
#             found = True
#             break
# print(sorted([(state, network[state]) for state, steps in finalstates]))

import math
print("p2:", math.lcm(*[steps for state, steps in finalstates]))
