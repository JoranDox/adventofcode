import string
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day03inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day03input.txt")) as f:
    data = f.read().strip()

def _neighbours(x,y):
    return {
        (x-1, y-1),
        (x-1, y),
        (x-1, y+1),
        (x, y-1),
        (x, y),
        (x, y+1),
        (x+1, y-1),
        (x+1, y),
        (x+1, y+1),
    }

def neighbours(xs,ys):
    neighset = set()
    for x in xs:
        for y in ys:
            neighset |= _neighbours(x,y)
    # print(f"neighbours for {xs}, {ys} = {neighset}")
    return neighset


numlocs = set()
symlocs = {}
gearlocs = set()
for y, line in enumerate(data.splitlines()):
    print(y,line)
    numaccum = 0
    xaccum = []
    for x, i in enumerate(line):
        if i == ".":
            if numaccum == 0:
                continue
            else:
                print(f"found {numaccum} at {xaccum}, {y}")
                numlocs |= {(numaccum, tuple(xaccum), y),}
                numaccum = 0
                xaccum = []
                continue
        elif i in string.digits:
            numaccum *= 10
            numaccum += int(i)
            xaccum.append(x)
        else: # i is a symbol
            if numaccum != 0:
                print(f"found {numaccum} at {xaccum}, {y}")
                numlocs |= {(numaccum, tuple(xaccum), y),}
                numaccum = 0
                xaccum = []

            print(f"found {i} at {(x,y)}")
            assert i != "\n"
            symlocs[(x,y)] = i

    if numaccum != 0:
        print(f"found {numaccum} at {xaccum}, {y}")
        numlocs |= {(numaccum, tuple(xaccum), y),}
        continue

print("numlocs", numlocs)
print("symlocs", symlocs)
print("symlocs_set", symlocs_set:= set(symlocs))
print("gearlocs", gearlocs)

nummap = {} # needed for part 2
numset_rev = {frozenset(neighbours(xs, (y,))): num for num, xs, y in numlocs}
# part 1
accump1 = 0
for num, xs, y in numlocs:
    neigh = neighbours(xs, (y,))
    for n in neigh:
        nummap[n] = num
    print("testing", num, xs, y)
    print(neigh)
    assert frozenset(neigh) in numset_rev
    assert numset_rev[frozenset(neigh)] == num
    if overlap:=(neigh & symlocs_set):
        print(f"adding {num} because {overlap}")
        accump1 += num
print(accump1)

# part 2
accump2 = 0
for loc, sym in symlocs.items():
    if sym == "*":
        adjacents = set()
        subaccum = 1
        for locs in numset_rev:
            if overlap:= ({loc} & locs):
                if locs not in adjacents:
                    adjacents |= {locs}
                    subaccum *= numset_rev[locs]
        if len(adjacents) == 2:
            print("ok:", loc, adjacents)
            accump2 += subaccum
        else:
            print("nok", loc, adjacents)
print(accump2)
# 41054866