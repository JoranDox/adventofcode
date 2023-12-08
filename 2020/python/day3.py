mymap = []
with open("day3input.txt") as infile:
    # with open("day3inputex.txt") as infile:
    for line in infile:
        mymap.append([c for c in line[:-1]])
# print(mymap)

maph, mapw = (len(mymap), len(mymap[0]))


def addpos(pa, pb, da, db):
    return (pa + da), (pb + db) % mapw


# def getmap(posa, posb):
#     return  mymap[posa][posb]


def printmap():
    for line in mymap:
        print("".join(line))


printmap()


def checkslope(diry, dirx):
    direction = (1, 3)

    posy, posx = (0, 0)

    treecount = 0
    emptycount = 0
    try:
        while True:
            posy, posx = addpos(posy, posx, diry, dirx)
            mymap[posy][posx]
            if mymap[posy][posx] == "#":
                treecount += 1
                # mymap[posy][posx] = "X"
            elif mymap[posy][posx] == ".":
                emptycount += 1
                # mymap[posy][posx] = "O"
    except IndexError:
        pass
    print("direction:", diry, dirx, "trees:", treecount, "empty:", emptycount)
    return treecount
    # printmap()


accum = 1
accum *= checkslope(1, 1)
accum *= checkslope(1, 3)
accum *= checkslope(1, 5)
accum *= checkslope(1, 7)
accum *= checkslope(2, 1)
print(accum)
