import numpy as np
import pandas as pd
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day12inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day12input.txt")) as f:
    data = f.read().strip()


def generate(p2):
    return ".".join(("#") * p for p in p2)


def shortengaps(p):
    while ".." in p:
        p = p.replace("..", ".")
    return p


def condense(p):
    assert "?" not in p
    p = p.strip(".")
    previous = False
    accum = []
    for i, char in enumerate(p):
        if previous and char == "#":
            accum[-1] += 1
        elif not previous and char == "#":
            accum.append(1)
            previous = True
        else:
            #char != "#"
            previous = False
    return tuple(accum)


total_accum = 0

def prefixmatch(partial, pattern):
    for i,j in zip(partial, pattern):
        if i > j:
            return False
    return True


def dynamicprogramming(ly, lx):
    # precondition: both include trailing & leading "."
    # lx does not contain "?"
    assert "?" not in lx
    if ly[0] != ".":
        ly = ["."] + list(ly)
    if ly[-1] != ".":
        ly = list(ly) + ["."]
    if lx[0] != ".":
        lx = ["."] + list(lx)
    if lx[-1] != ".":
        lx = list(lx) + ["."]
    # print(ly)
    # print(lx)
    dmap = [[" " for n in lx] for m in ly]
    maxx = len(lx)-1
    maxy = len(ly)-1
    # print(maxx, maxy)
    dmap[0][0] = 1

    def printmap():
        print()
        print(pd.DataFrame(np.array(dmap), columns=list(lx), index=list(ly)))
        
    # printmap()

    # mark top & bottom impossible locations
    for n in range(1, len(dmap[0])):
        dmap[0][n] = "x"
    newxs = [(x, 0) for x in range(1,maxx)]

    dmap[-1] = ["x" for _ in dmap[-1]]
    newxs += [(x, maxy) for x in range(maxx)]
    dmap[-1][-1] = " "
    # printmap()

    # mark impossible matches
    for y, chary in enumerate(ly):
        if chary == "?":
            continue
        for x, charx in enumerate(lx):
            if charx != chary:
                dmap[y][x] = "x"
                newxs.append((x,y))

    for x,y in newxs:
        # print(x,y)
        assert dmap[y][x] == "x", (x,y)

    # printmap()

    def donewxs():
        while newxs:
            x,y = newxs.pop()
            # print("checking",x,y)
            if y != 0:
                # look up
                if x != 0:
                    # look to the left to maybe x top left
                    #  ..    x.
                    #  xX -> xX
                    if dmap[y][x-1] == "x" and dmap[y-1][x-1] != "x":
                        dmap[y-1][x-1] = "x"
                        newxs.append((x-1, y-1))
                if x != maxx:
                    # look to the right to maybe x top
                    #  ..    x.
                    #  Xx -> Xx
                    if dmap[y][x+1] == "x" and dmap[y-1][x] != "x":
                        dmap[y-1][x] = "x"
                        newxs.append((x, y-1))
            if y != maxy:
                # look down
                if x != 0:
                    # look to the left to maybe x bot
                    #  xX -> xX
                    #  ..    .x
                    if dmap[y][x-1] == "x" and dmap[y+1][x] != "x":
                        dmap[y+1][x] = "x"
                        newxs.append((x, y+1))
                if x != maxx:
                    # look to the right to maybe x bot right
                    #  Xx -> Xx
                    #  ..    .x
                    if dmap[y][x+1] == "x" and dmap[y+1][x+1] != "x":
                        dmap[y+1][x+1] = "x"
                        newxs.append((x+1, y+1))
    donewxs()
    # do all others
    # printmap()
    
    for y, chary in list(enumerate(ly))[1:]: # skip top row
        for x, charx in enumerate(lx):
            chard = dmap[y][x]
            accum = 0
            if chard == "x":
                # already crossed off
                continue
            if x != 0:
                # always look top left if x != 0
                temp = dmap[y-1][x-1]
                if temp != "x":
                    accum += temp
            
            if y != 0 and charx != "#":
                # look up when not "#"
                temp = dmap[y-1][x]
                if temp != "x":
                    accum += temp

            if accum != 0:
                dmap[y][x] = accum
            else:
                dmap[y][x] = "x"
                newxs.append((x,y))
                donewxs()
    # printmap()
    return accum # last accum is the result I think?


# if p1: multiplier = 1
# if p2: multiplier = 5
multiplier = 5
p1accum = 0
for line in data.splitlines():
    # print(line)
    pattern1, pattern2 = line.split()
    pattern1 = "?".join([pattern1] * multiplier)
    pattern1 = shortengaps(pattern1)
    pattern2 = tuple(int(i) for i in pattern2.split(",")) * multiplier
    # print(pattern1, pattern2)
    l = len(pattern1)
    minimum = sum(pattern2) + len(pattern2) - 1
    # print( "|", l, minimum, pattern1.count("#"), pattern1.count("#") + pattern1.count("?"))
    dof = l - minimum
    ######## p1 naive code
    # patterns = [()]
    # for i, symbol in enumerate(pattern1):
    #     if symbol == "?":
    #         patterns = [
    #             newp for p in patterns if prefixmatch(condense("".join(newp := (p + (".",)))),pattern2)
    #         ] + [
    #             newp for p in patterns if prefixmatch(condense("".join(newp := (p + ("#",)))),pattern2)
    #         ]
    #     else:
    #         patterns = [
    #             newp for p in patterns if prefixmatch(condense("".join(newp := (p + (symbol,)))),pattern2)
    #         ]

    #     # pset = {condense("".join(p)) for p in patterns}
    # paccum = 0
    # for p in patterns:

    #     # print(p, condense("".join(p)), pattern2)
    #     if condense("".join(p)) == pattern2:
    #         # print(p)
    #         paccum += 1
    #         # print("   yes: ", p)
    # #     print("   ", "".join(condense(p)))
    # # print(paccum)
    # total_accum += paccum
    # print(total_accum)
    ######## end p1 naive code
    # print("".join(generate(pattern2)))
    p1accum += dynamicprogramming(pattern1, generate(pattern2))


    # 16384 = 2**14
    # 2500 = 5*5*5*5 * 4
    # 506250 = 2 * 3**4 * 5**5
print(p1accum)