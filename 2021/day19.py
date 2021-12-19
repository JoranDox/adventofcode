import numpy as np

# with open("day19inputtest.txt") as f:
with open("day19input.txt") as f:
    data = f.read().strip()

scanners = []
for line in map(lambda s: s.strip(),data.splitlines()):
    # print(line)
    if line.startswith("--- scanner "):
        scanners.append([])
    elif line:
        t = list(map(int,line.split(",")))
        while len(t) < 3:
            t.append(0)
        scanners[-1].append(tuple(t))
    else:
        pass

# print(scanners)

def orientations(inp):
    x,y,z = inp

    # pos/neg
    ors = [
        (x,y,z),
        (-x,y,z),
        (x,-y,z),
        (x,y,-z),
        (x,-y,-z),
        (-x,y,-z),
        (-x,-y,z),
        (-x,-y,-z),
    ]

    # order
    ret = []
    for x,y,z in ors:
        ret.extend([
            (x,y,z),
            (x,z,y),
            (y,x,z),
            (z,x,y),
            (y,z,x),
            (z,y,x),
        ])
    # somehow the spec says only 24, but I get 48 unique ones?
    return ret


def getnextscanner(scannerqueue, foundbeacons, correctscanners, depth=0):
    print("depth", depth)
    # s = scannerqueue[0]
    for si, s in enumerate(scannerqueue):
        nextqueue = [*scannerqueue[:si], *scannerqueue[si+1:]]
        # beacons is all points oriented in the same way
        for ornum, beacons in enumerate(zip(*(orientations(v) for v in s))):
            # print(depth, ornum)
            for ijknum, (ijkx, ijky, ijkz) in enumerate(foundbeacons):
                for ijk2num, (bijkx, bijky, bijkz) in enumerate(beacons):
                # print(depth, ornum, ijknum)
                    ijkbeacons = [
                        (
                            x - bijkx + ijkx,
                            y - bijky + ijky,
                            z - bijkz + ijkz,
                        )
                        for x,y,z in beacons
                    ]
                    scannerpos = (
                            - bijkx + ijkx,
                            - bijky + ijky,
                            - bijkz + ijkz,
                    )
                    # print(beacons)
                    b = set(ijkbeacons)
                    # print(b)
                    c = len(foundbeacons & b)
                    # print(foundbeacons & b)
                    # print(c)
                    assert c >= 1, "we literally forced this"

                    # this is a good orientation
                    if c >= 12:
                        print("yay", c, "matched")
                        # if this isn't the last scanner
                        if len(nextqueue) >= 1:
                            r = getnextscanner(nextqueue, foundbeacons | b, (*correctscanners, scannerpos), depth+1)
                            if r:
                                return r
                            else:
                                # dead end, try next orientation
                                continue
                        else:
                            print("we found them all")
                            return foundbeacons | b, (*correctscanners, scannerpos)
                # else: try another orientation
    # if we get here, we failed
    print("back to depth", depth-1)
    return None

n, correctscanners = getnextscanner(scanners[1:], set(scanners[0]), ((0,0,0),))
print(n,len(n))

maxdist = 0
for x1, y1, z1 in correctscanners:
    for x2, y2, z2 in correctscanners:
        dist = abs(x1-x2) + abs(y1-y2) + abs(z1-z2)
        if dist > maxdist:
            maxdist = dist
            print(maxdist)