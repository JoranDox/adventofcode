import collections
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day21inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day21input.txt")) as f:
    data = f.read().strip()

dones = {}
todos = collections.deque()
ops = {
    "+": (lambda x,y: x+y),
    "-": (lambda x,y: x-y),
    "*": (lambda x,y: x*y),
    "/": (lambda x,y: x//y),
}
for line in data.splitlines():
    name, rest = line.split(": ")
    if " " not in rest:
        dones[name] = int(rest)
    else:
        todos.append((name, rest.split()))

while todos:
    name, (lhs, op, rhs) = todos.popleft()
    if lhs in dones and rhs in dones:
        dones[name] = ops[op](dones[lhs],dones[rhs])
        print(f"{name} = {lhs} {op} {rhs} = {dones[name]}")
    else:
        todos.append((name, (lhs, op, rhs)))
    if "root" in dones:
        print("p1:", dones["root"])
        break

# p2:
facts = {}
unknown = collections.deque()
opinverse = {
    "+": "-",
    "-": "+",
    "*": "/",
    "/": "*",
}
for line in data.splitlines():
    print(line)
    name, rest = line.split(": ")
    if name == "humn":
        # skip for now
        continue
    if " " not in rest:
        facts[name] = int(rest)
    else:
        lhs, op, rhs = rest.split()
        if name == "root":
            rootlhs = lhs
            rootrhs = rhs
            continue
        else:
            unknown.append((name, (lhs, op, rhs)))

print(unknown)
changed = len(unknown)
while changed:
    changed -= 1
    name, (lhs, op, rhs) = unknown.popleft()

    if lhs in facts:
        lhs = facts[lhs]
    if rhs in facts:
        rhs = facts[rhs]

    if (type(lhs) == int) and (type(rhs) == int):
        changed = len(unknown)
        facts[name] = ops[op](lhs,rhs)
        print(f"{name} = {lhs} {op} {rhs} = {facts[name]}")
        continue

    unknown.append((name, (lhs, op, rhs)))

unknowndict = {
    name: (lhs, op, rhs) for name, (lhs, op, rhs) in unknown
}
print(unknown)
print(unknowndict)
print(facts)
print("root =", rootlhs, "==", rootrhs)

indict = 0
if rootlhs in unknowndict:
    indict += 1
if rootrhs in unknowndict:
    indict += 1
assert indict == 1

# isolate humn to the left
if rootrhs in unknowndict:
    rootlhs, rootrhs = rootrhs, rootlhs

assert rootrhs in facts
rootrhs = facts[rootrhs]
assert rootlhs in unknowndict
unknowndict["humn"] = "sentinel value"
while rootlhs != "humn":
    print(rootlhs, "=", rootrhs)
    left, op, right = unknowndict[rootlhs]
    print(rootlhs, "=", left, op, right, "=", rootrhs)
    if left in unknowndict and type(right) == int:
        # left is unknown
        # no problem
        #     x + a = b
        # <=> x = b - a
        #     x - a = b
        # <=> x = b + a
        #     x * a = b
        # <=> x = b / a
        #     x / a = b
        # <=> x = b * a
        rootrhs = ops[opinverse[op]](rootrhs,right)
        rootlhs = left
        continue

    # right is unknown
    assert right in unknowndict and type(left) == int, (left, op, right, rootrhs)
    rootlhs = right
    if op == "+" or op == "*":
        # no problem
        #     a * x = b
        # <=> x = b / a
        #     a + x = b
        # <=> x = b - a
        rootrhs = ops[opinverse[op]](rootrhs,left)
    else:
        # inversion
        if op in ("/", "-"):
            #     a / x = b
            # <=> x = a / b
            #     a - x = b
            # <=> x = a - b
            rootrhs = ops[op](left, rootrhs)

print("p2:", rootrhs)