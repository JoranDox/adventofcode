import collections
import operator
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day19inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day19input.txt")) as f:
    data = f.read().strip()


workflows, items = data.split("\n\n")

wfs = {}
for line in workflows.splitlines():
    name, wf = line.split("{")
    assert wf[-1] == "}"
    subwfs = wf[:-1].split(",")
    lwf = []
    for subwf in subwfs:
        if ":" in subwf:
            test, nxt = subwf.split(":")
            if ">" in subwf:
                testkey, val = test.split(">")
                intval = int(val)
                # print(f"item[{testkey}] > {intval} -> {nxt}")
                lwf.append((testkey, operator.gt, intval, nxt))
            elif "<" in subwf:
                testkey, val = test.split("<")
                intval = int(val)
                # print(f"item[{testkey}] < {intval} -> {nxt}")
                lwf.append((testkey, operator.lt, intval, nxt))
            else:
                panik
        else:
            # final step
            lwf.append(("x", lambda *x: True, 0, subwf))
    wfs[name] = lwf
# print(wfs)
accum = 0
for item in items.splitlines():
    xmas = {k:int(v) for k,v in
        [v.split("=") for v in item[1:-1].split(",")]
    }
    # print(xmas)
    cur = "in"
    while cur not in ("A","R"):
        wf = wfs[cur]
        for testkey, op, intval, nxt in wf:
            # lwf.append((lambda item, intval=intval: item[testkey] < intval, nxt))
            if op(xmas[testkey], intval):
                cur = nxt
                # print(cur)
                break
    if cur == "A":
        accum += sum(xmas.values())
    # else:
        # print("no")
print("p1:",accum)

## p2: reverse, reverse

starter = ({
    "x": (1, 4000),
    "m": (1, 4000),
    "a": (1, 4000),
    "s": (1, 4000),
}, "in", 0)

def okrange(minkey, maxkey):
    return minkey <= maxkey

accump2 = 0
notaccump2 = 0
states = collections.deque()
states.append(starter)
while states:
    allowedvalues, state, step = states.popleft()
    if state in ("A", "R"):
        # do the maybe ending math
        if state == "A":
            subaccum = 1
            for minkey,maxkey in allowedvalues.values():
                subaccum *= (maxkey - minkey + 1)
            accump2 += subaccum
        elif state == "R":
            # pass # don't add to accump2
            subaccum = 1
            for minkey,maxkey in allowedvalues.values():
                subaccum *= (maxkey - minkey + 1)
            notaccump2 += subaccum
            notaccump2
        else:
            panik
        continue

    testkey, op, intval, nxt = wfs[state][step]
    minkey, maxkey = allowedvalues[testkey]
    if op == operator.gt:
        lhs = minkey, intval
        rhs = intval+1, maxkey
        if okrange(*rhs):
            states.append(({**allowedvalues, **{testkey: rhs}}, nxt, 0))
        if okrange(*lhs):
            states.append(({**allowedvalues, **{testkey: lhs}}, state, step+1))
    elif op == operator.lt:
        lhs = minkey, intval-1
        rhs = intval, maxkey
        if okrange(*lhs):
            states.append(({**allowedvalues, **{testkey: lhs}}, nxt, 0))
        if okrange(*rhs):
            states.append(({**allowedvalues, **{testkey: rhs}}, state, step+1))
    else:
        states.append((allowedvalues, nxt, 0))

# print("p2debug:", accump2, notaccump2, accump2 + notaccump2)
print("p2:", accump2)