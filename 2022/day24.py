import collections
import time
import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day24inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day24input.txt")) as f:
    data = f.read().strip()

directions_str = {
    ".": (0, 0, 0, 0),  # empty
    "^": (1, 0, 0, 0),  # "N"
    ">": (0, 1, 0, 0),  # "E"
    "v": (0, 0, 1, 0),  # "S"
    "<": (0, 0, 0, 1),  # "W"
}

# directions_tup = [
#     ( 0, -1), # "N"
#     ( 1,  0), # "E"
#     ( 0,  1), # "S"
#     (-1,  0), # "W"
# ]

directions_rep = {
    (0, 0, 0, 0): " ",  # empty, 0
    (1, 0, 0, 0): "↑",  # N, 1
    (0, 1, 0, 0): "→",  # E, 2
    (1, 1, 0, 0): "⇗",  # NE, 3
    (0, 0, 1, 0): "↓",  # S, 4
    (1, 0, 1, 0): "⇅",  # SN, 5
    (0, 1, 1, 0): "⇘",  # SE, 6
    (1, 1, 1, 0): "↠",  # SNE, 7
    (0, 0, 0, 1): "←",  # W, 8
    (1, 0, 0, 1): "⇖",  # WN, 9
    (0, 1, 0, 1): "⇄",  # WE, 10
    (1, 1, 0, 1): "↟",  # WNE, 11
    (0, 0, 1, 1): "⇙",  # WS, 12
    (1, 0, 1, 1): "↞",  # WSN, 13
    (0, 1, 1, 1): "↡",  # WSE, 14
    (1, 1, 1, 1): "↻",  # WSNE, 15
}

for i, d in enumerate(directions_rep):
    assert int("".join([str(_) for _ in d[::-1]]), 2) == i, (i, d)

blizzardmap = {}
maxy = 0
maxx = 0
for y, line in enumerate(data.splitlines()[1:-1]):
    for x, char in enumerate(line[1:-1]):
        blizzardmap[(x, y)] = directions_str.get(char, char)
        maxy = max(maxy, y)
        maxx = max(maxx, x)

print(maxx, maxy)

# print(blizzardmap)
# globals
minx = 0
miny = 0
entryloc = (0, -1)
exitloc = (maxx, maxy + 1)


def printmap(lazymap):
    for y in range(miny - 1, maxy + 2):
        # print(y)
        for x in range(minx - 1, maxx + 2):
            # print(x)
            if (x, y) in lazymap:
                tup = lazymap[(x, y)]
                if type(tup) == tuple:
                    tup = directions_rep[tup]
                print(tup, end="")
            elif (x, y) in (entryloc, exitloc):
                # in & out tiles
                print(" ", end="")
            # walls
            # ┗┓┏┛
            elif x == minx - 1 and y == miny - 1:
                print("┏", end="")
            elif x == maxx + 1 and y == miny - 1:
                print("┓", end="")
            elif x == minx - 1 and y == maxy + 1:
                print("┗", end="")
            elif x == maxx + 1 and y == maxy + 1:
                print("┛", end="")
            elif x == minx - 1 or x == maxx + 1:
                print("┃", end="")
            elif y == miny - 1 or y == maxy + 1:
                print("━", end="")
            else:
                # empty space
                print(" ", end="")
        print()
    print()


printmap(blizzardmap)


def neg(v):
    return tuple(-x for x in v)


def vsum(*v):
    return tuple(sum(x) for x in zip(*v))


def vmod(v, m):
    # positive-only mod
    return tuple(((v_ + m_) % m_) for v_, m_ in zip(v, m))


def vmul(v, num):
    return tuple(int(vx * num) for vx in v)


directions_tup = [
    (0, -1),  # "N"
    (1, 0),  # "E"
    (0, 1),  # "S"
    (-1, 0),  # "W"
]

blizzards = [
    [frozenset([k for k, v in blizzardmap.items() if v == (1, 0, 0, 0)])],
    [frozenset([k for k, v in blizzardmap.items() if v == (0, 1, 0, 0)])],
    [frozenset([k for k, v in blizzardmap.items() if v == (0, 0, 1, 0)])],
    [frozenset([k for k, v in blizzardmap.items() if v == (0, 0, 0, 1)])],
]


def nextminute(locset, direction):
    # print(locset)
    # print(direction)
    return frozenset(
        [
            vmod(vsum(loc, direction), (maxx + 1, maxy + 1))  # :thinking:
            for loc in locset
        ]
    )


def onehot(num, tlen=4):
    return tuple([(1 if i == num else 0) for i in range(tlen)])


def bliztomap(locset, index):
    return {k: onehot(index, 4) for k in locset}


# curdirection = 3
# print(blizzards[curdirection][0])
# # print(bliztomap(blizzards[curdirection][0],curdirection))
# printmap(bliztomap(blizzards[curdirection][0],curdirection))
# print(nextminute(blizzards[curdirection][0],directions_tup[curdirection]))
# printmap(bliztomap(nextminute(blizzards[curdirection][0],directions_tup[curdirection]),curdirection))


stop = [False, False, False, False]
while not all(stop):
    for i in range(4):
        if not stop[i]:
            timelocset = blizzards[i]
            # print("before:")
            # printmap(bliztomap(timelocset[-1],i))
            direction = directions_tup[i]
            nm = nextminute(timelocset[-1], direction)
            # print("after:")
            # printmap(bliztomap(nm,i))
            if nm == timelocset[0]:
                stop[i] = True
                break
            timelocset.append(nm)

    # for i in blizzards:
    #     print(i)

# print([len(i) for i in blizzards])
assert not (len(blizzards[0]) % (maxy + 1)), (len(blizzards[0]), (maxy + 1))
assert not (len(blizzards[1]) % (maxx + 1)), (len(blizzards[1]), (maxx + 1))
assert not (len(blizzards[2]) % (maxy + 1)), (len(blizzards[2]), (maxy + 1))
assert not (len(blizzards[3]) % (maxx + 1)), (len(blizzards[3]), (maxx + 1))


def gettimeslice(multitimelocset, t, printable=False):
    slices = [timelocset[t % len(timelocset)] for timelocset in multitimelocset]
    keys = set()
    for locset in slices:
        keys |= locset
    if printable:
        return {
            k: vsum(
                *[
                    bliztomap(locset, i).get(k, (0, 0, 0, 0))
                    for i, locset in enumerate(slices)
                ]
            )
            for k in keys
        }
    else:
        return keys


# print(gettimeslice(blizzards,0))
# import time
# t0 = time.time()
# # printableslices = gettimeslice(blizzards,1,printable=True), gettimeslice(blizzards,2,printable=True), gettimeslice(blizzards,3,printable=True)
# t1 = time.time()
# print(t1 - t0)
# t0 = time.time()
# # printmap(printableslices[0])
# # printmap(printableslices[1])
# # printmap(printableslices[2])
# t1 = time.time()
# print(t1 - t0)
# t0 = time.time()
# slices = gettimeslice(blizzards,1), gettimeslice(blizzards,2), gettimeslice(blizzards,3)
# t1 = time.time()
# print(t1 - t0)
# find max time slice

# ugly LCM, cba
t0 = gettimeslice(blizzards, 0)
for ltime in range(len(blizzards[0]) * len(blizzards[1])):
    if gettimeslice(blizzards, ltime + 1) == t0:
        print(ltime + 1)
        looptime = ltime + 1
        assert ltime + 1 // len(blizzards[0])
        assert ltime + 1 // len(blizzards[1])
        break


def manhattandistance(l1, l2):
    return sum([abs(z1 - z2) for z1, z2 in zip(l1, l2)])


def solutiononeway(entryloc, exitloc, starttime=0):
    seenloctimes = set()

    maxdist = manhattandistance(entryloc, exitloc)
    priolisttodo = collections.defaultdict(list)

    totallocations = 0
    for i in range(looptime):
        # add all possible waits to the prioqueue, so we can avoid x<0 later on
        priolisttodo[maxdist + i + starttime].append((entryloc, i + starttime))
        seenloctimes |= {(entryloc, i)}
        locs = (maxx + 1) * (maxy + 1) - len(gettimeslice(blizzards, i))
        totallocations += locs + 1  # for the start loc
        print(i, locs)

    print("total locations:", totallocations)

    # mintime = None
    # highesttimeseen = 0
    # numstatesseen = 1
    # queueseen = 1
    # 190 too low
    # 729 (?) too high
    # 1150 too high
    steps = 0
    tstart = time.time()
    while priolisttodo:
        l = priolisttodo[min(priolisttodo)]
        if not l:
            # print("=== going from:", min(priolisttodo))
            del priolisttodo[min(priolisttodo)]
            # print("=== to",min(priolisttodo))
            continue
        loc, ltime = l.pop()
        steps += 1
        t = ltime + 1
        # print("checking:", loc, "at time:", time)
        # if mintime is not None:
        #     if t >= mintime:
        #         continue # skip this one
        # if t > highesttimeseen:
        #     highesttimeseen = t
        #     print("seen times:", t, len(priolisttodo), steps, time.time()-tstart, steps / (time.time()-tstart))
        # if len(priolisttodo) > queueseen * 2:
        #     queueseen = len(priolisttodo)
        #     print("seen queue:", t, len(priolisttodo), steps, time.time()-tstart, steps / (time.time()-tstart))
        # if len(seenloctimes) > numstatesseen * 2:
        #     numstatesseen = len(seenloctimes)
        #     print("seen states:", t, len(seenloctimes), steps, time.time()-tstart, steps / (time.time()-tstart))
        if steps % 10000 == 0:
            print(
                "seen steps:",
                t,
                len(seenloctimes),
                steps,
                time.time() - tstart,
                steps / (time.time() - tstart),
            )

        for direction in [(0, 0)] + directions_tup:
            # print(direction)
            sx, sy = vsum(loc, direction)
            # print(direction, (sx,sy))
            if (sx, sy) == exitloc:
                # print("found!")
                # print("at time:", t)
                return t
                # if t < mintime:
                #     print("found!")
                #     print("at time:", t)
                #     mintime = t
            suggestion = ((sx, sy), t)
            sugloop = ((sx, sy), t % looptime)
            if (
                (sx, sy) not in gettimeslice(blizzards, t)
                and (0 <= sx <= maxx and 0 <= sy <= maxy)
                and sugloop not in seenloctimes
            ):
                # if (sx,sy) == (2,2):
                #     print(sugloop)
                # print(seenloctimes)
                seenloctimes |= {sugloop}
                priolisttodo[manhattandistance((sx, sy), exitloc) + t].append(
                    suggestion
                )
                # print("adding state: going from", loc, "to", suggestion)


p1 = solutiononeway(entryloc, exitloc, starttime=0)
print("p1:", p1)
pback = solutiononeway(exitloc, entryloc, starttime=p1)
print("p2 going back:", pback - p1)
p2 = solutiononeway(entryloc, exitloc, starttime=pback)
print("p1:", p1)
print("p2 going back:", pback - p1)
print("p2 going ahead again:", p2 - pback)
print("p2 total:", p2)
