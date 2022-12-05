
import pathlib
parent_directory = pathlib.Path(__file__).resolve().absolute().parent
# with open(parent_directory.joinpath("day05inputtest.txt")) as f:
with open(parent_directory.joinpath("day05input.txt")) as f:
    data = f.read()


config, moves = data.split("\n\n")

def pad(twodstr):
    m = max([len(c) for c in twodstr])

    return [
        l + (m - len(l)) * ' '
        for l in twodstr
    ]
# print(config)
# print(pad(config.splitlines()))

def doday5(config, moves, p2=False):
    stacks = {}
    for header, *blocks in zip(*reversed(pad(config.splitlines()))):
        # print(f"h: {header}, b:{blocks}")
        if header != " ":
            stacks[header] = [b for b in blocks if b != " "]

    # print(stacks)
    for line in moves.splitlines():
        _, num, _, fromstack, _, tostack = line.split()
        popped = []
        for i in range(int(num)):
            popped.append(stacks[fromstack].pop())
        if p2:
            popped = reversed(popped)
        stacks[tostack].extend(popped)
    # print(stacks)

    print("p2: ", end="")
    for i in range(len(stacks)):
        print(stacks[str(i+1)][-1],end="")
    print()

doday5(config, moves)
doday5(config, moves, p2=True)