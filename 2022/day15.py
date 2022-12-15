
import pathlib
parent_directory = pathlib.Path(__file__).resolve().absolute().parent
# with open(parent_directory.joinpath("day15inputtest.txt")) as f:
with open(parent_directory.joinpath("day15input.txt")) as f:
    data = f.read().strip()

parsed = []

for line in data.splitlines():
    (_, _, sx, sy, _, _, _, _, bx, by) = line.split()
    parsed.append(
        (
            int(sx.split("=")[1].split(",")[0]),
            int(sy.split("=")[1].split(":")[0]),
            int(bx.split("=")[1].split(",")[0]),
            int(by.split("=")[1]),
        )
    )

def manhattandistance(l1,l2):
    return sum([abs(z1-z2) for z1,z2 in zip(l1,l2)])

# print(manhattandistance((1,2),(-5,8)))

sensors = [(sx,sy) for sx,sy,bx,by in parsed]
beacons = [(bx,by) for sx,sy,bx,by in parsed]
closest = {(sx,sy):manhattandistance((sx,sy),(bx,by)) for sx,sy,bx,by in parsed}
print(sensors)
print(closest)

minx = min(
    min([x for x,y in sensors]),
    min([x for x,y in beacons])
)
maxx = max(
    max([x for x,y in sensors]),
    max([x for x,y in beacons])
)
miny = min(
    min([y for x,y in sensors]),
    min([y for x,y in beacons])
)
maxy = max(
    max([y for x,y in sensors]),
    max([y for x,y in beacons])
)
maxd = max(closest.values())

def inrange(x,y):
    for (sx,sy),d in closest.items():
        if manhattandistance((sx,sy),(x,y)) <= d:
            return ((sx,sy),d)
    return False

def first(rownum):
    m = None
    for (sx,sy),d in closest.items():
        if abs(sy - rownum) <= d:
            m2 = sx + abs(sy - rownum) - d
            if m is None:
                m = m2
            else:
                m = min(m,m2)
    return m

def last(rownum):
    m = None
    for (sx,sy),d in closest.items():
        if abs(sy - rownum) <= d:
            m2 = sx - abs(sy - rownum) + d
            if m is None:
                m = m2
            else:
                m = max(m,m2)
    return m


def retoverlap(cmin,cmax,c1,c2):
    if (c2 < (cmin -1)) or (c1 > (cmax + 1)):
        # no overlap
        return False
    elif (
        (c1 <= cmin-1 <= c2)
        or (c1 <= cmax+1 <= c2)
        or (c1 >= cmin and c2 <= cmax)
    ):
        # overlap
        return (min(c1,cmin),max(c2,cmax))
    else:
        print("missing case:", cmin,cmax,c1,c2)


def rowranges(rownum):
    m = []
    for (sx,sy),d in closest.items():
        if abs(sy - rownum) <= d: # sensor hits row
            sx_min = sx + abs(sy - rownum) - d
            sx_max = sx - abs(sy - rownum) + d
            m.append((sx_min,sx_max))

    m2 = []
    while m:
        cmin, cmax = m.pop()
        changed = True
        while changed:
            changed = False
            newm = []
            for c1, c2 in m:
                overlap = retoverlap(cmin,cmax,c1,c2)
                if overlap:
                    changed = True
                    cmin, cmax = overlap
                else:
                    newm.append((c1,c2))
            m = newm
        m2.append((cmin,cmax))
    # print(m2)
    return m2


def printmap():
    print("   ", end="")
    for x in range(minx - maxd, maxx+maxd+1):
        print(str(x).rjust(3), end="")
    print()
    for y in range(miny - maxd,maxy+maxd+1):
        print(str(y).rjust(3), end=" ")
        for x in range(minx - maxd, maxx+maxd+1):
            if (x,y) in sensors:
                print(" S",end=" ")
            elif (x,y) in beacons:
                print(" B",end=" ")
            else:
                if inrange(x,y):
                    print(" #",end=" ")
                else:
                    print(" .",end=" ")
        print(" ", y, first(y), last(y), rowranges(y), end=" ")
        print()
    print()

def count(y):
    counter = 0
    for x in range(first(y), last(y)+1):
        if (x,y) in sensors:
            pass
        elif (x,y) in beacons:
            pass
        else:
            if inrange(x,y):
                counter += 1
    return counter

def find(searchrange):
    for y in range(searchrange):
        rr = rowranges(y)
        if len(rr) > 1:
            assert len(rr) == 2
            (_, i1), (i2, _) = sorted(rr)
            assert i2 - i1 == 2
            return i1 + 1, y

def sensoredge(sx,sy,d):
    left = sx - d - 1, sy
    right = sx + d + 1, sy
    top = sx, sy - d - 1
    bottom = sx, sy + d + 1
    # print(left,right,top,bottom)
    edges = set()
    for i in range(d+2):
        edges |= {
            (left[0] + i, left[1] - i),
            (left[0] + i, left[1] + i),
            (right[0] - i, right[1] - i),
            (right[0] - i, right[1] + i),
        }
    return edges

print(sensoredge(0,0,2))

def find2(searchrange):
    edges = set()
    for (sx,sy),d in closest.items():
        edges |= sensoredge(sx,sy,d)
    # print(len(edges))
    for x,y in edges:
        if 0 < x < searchrange and 0 < y < searchrange:
            rr = rowranges(y)
            if len(rr) > 1:
                assert len(rr) == 2
                (_, i1), (i2, _) = sorted(rr)
                assert i2 - i1 == 2
                return i1 + 1, y

def find3(searchrange):
    edges = set()
    for (sx,sy),d in closest.items():
        edges |= sensoredge(sx,sy,d)
    # print(len(edges))
    for x,y in edges:
        if 0 < x < searchrange and 0 < y < searchrange and not inrange(x,y):
            return x,y

import time

t0 = time.time()
# p1 (naive & slow but fast enough for part 1)
if maxd < 100:
    row = 10
    printmap()
else:
    row = 2000000
rr = rowranges(row)[0]
# print(rr)
t1 = time.time()
print(rr[1] - rr[0], t1 - t0)
# counter = count(y=row)
# print(counter)
# 6078701

# p2
if maxd < 100:
    searchrange = 20
    printmap()
else:
    searchrange = 4000000

t0 = time.time()
x,y = find(searchrange)
t1 = time.time()
print(x * 4000000 + y, t1 - t0)

t0 = time.time()
x,y = find2(searchrange)
t1 = time.time()
print(x * 4000000 + y, t1 - t0)

t0 = time.time()
x,y = find3(searchrange)
t1 = time.time()
print(x * 4000000 + y, t1 - t0)

# 68843501
#  4000000