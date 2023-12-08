import copy

infilename = "day20input.txt"
# infilename = "day20inputex.txt"

tiles = {}
with open(infilename) as infile:
    for part in infile.read().strip().split("\n\n"):
        part_split = [p.strip() for p in part.strip().split("\n")]
        num = part_split[0]
        assert num.startswith("Tile ") and num.endswith(":")
        num = int(num[5:-1])
        tiles[num] = [[t for t in tile] for tile in part_split[1:]]


def printfloormap(floormap):
    # print(floormap)
    print("\n".join("".join(line) for line in floormap))
    print()


def flipv(tile):
    return list(reversed(tile))


def rotate(tile):
    newtile = copy.deepcopy(tile)  # please be square
    dims = len(tile)
    for i in range(dims):
        # vertical
        for j in range(dims):
            # horizontal
            newtile[dims - j - 1][i] = tile[i][j]
    return newtile


def getborders(tile):
    tile_r = tile
    borders = []
    for _ in range(4):
        tile_r = rotate(tile_r)
        borders.append(tile_r[0])
        borders.append(flipv(tile_r)[0])
    return borders


# for num, tile in tiles.items():
#     print(num)
#     printfloormap(tile)

# printfloormap(tiles[2311])
# printfloormap(rotate(rotate(rotate(rotate(tiles[2311])))))
# print(["".join(b) for b in getborders(tiles[2311])])


def bordertonum(border):
    return int("".join(border).replace("#", "1").replace(".", "0"), 2)


# print([bordertonum(b) for b in getborders(tiles[2311])])

counter = {}
tileborders = {}
for tile in tiles:
    borders = set([bordertonum(b) for b in getborders(tiles[tile])])
    tileborders[tile] = borders
    for b in borders:
        if b in counter:
            counter[b] += 1
        else:
            counter[b] = 1

bordernums = set()
cornernums = set()
bordernums2 = set()
print(counter)
onlyonce = [k for k, v in counter.items() if v == 1]
for k in onlyonce:
    for tilenum, borders in tileborders.items():
        if k in borders:
            if tilenum in bordernums2:
                cornernums |= set([tilenum])
            elif tilenum in bordernums:
                bordernums2 |= set([tilenum])
            else:
                bordernums |= set([tilenum])
print(f"{bordernums=}")
print(f"{cornernums=}")
accum = 1
for num in cornernums:
    accum *= num
print(f"{accum=}")
print()
print("part 2")
print()

print(len(tiles))
sqrttiles = int(pow(len(tiles), 0.5))
bigpicturedims = 10 * sqrttiles
bigpicture = []
for i in range(bigpicturedims):
    l = []
    for j in range(bigpicturedims):
        l.append("_")
    bigpicture.append(l)
printfloormap(bigpicture)

cleanpicturedims = 8 * sqrttiles
cleanpicture = []
for i in range(cleanpicturedims):
    l = []
    for j in range(cleanpicturedims):
        l.append("_")
    cleanpicture.append(l)
printfloormap(cleanpicture)

startingcornernum = list(cornernums)[0]
startingcorner = tiles[startingcornernum]
del tiles[startingcornernum]


def fillbigpicture(tile, bigx, bigy):
    for y in range(1, len(tile) - 1):
        for x in range(1, len(tile) - 1):
            cleanpicture[bigy * 8 + y - 1][bigx * 8 + x - 1] = tile[y][x]
    for y in range(len(tile)):
        for x in range(len(tile)):
            bigpicture[bigy * 10 + y][bigx * 10 + x] = tile[y][x]


# printfloormap(tiles[2311])
# printfloormap(rotate(tiles[2311]))

for _ in range(4):
    if (bordertonum(startingcorner[0]) in onlyonce) and (
        bordertonum(rotate(startingcorner)[0]) in onlyonce
    ):
        # we found a correct top right corner
        fillbigpicture(startingcorner, sqrttiles - 1, 0)
    else:
        startingcorner = rotate(startingcorner)
printfloormap(startingcorner)
printfloormap(bigpicture)
printfloormap(cleanpicture)

latesttile = startingcorner


indexx = sqrttiles - 2


def getorientations(tile):
    ret = []
    for _ in range(4):
        tile = rotate(tile)
        for _ in range(2):
            tile = flipv(tile)
            ret.append(tile)
    return ret


def findleft(tiles, leftside):
    for tilenum, tile in tiles.items():
        for tile in getorientations(tile):
            if bordertonum(rotate(tile)[0]) == leftside:
                # we found a correct left side
                print("found left")
                return tilenum, tile


def finddown(tiles, downside):
    for tilenum, tile in tiles.items():
        for tile in getorientations(tile):
            if bordertonum(tile[0]) == downside:
                # we found a correct down side
                print("found down")
                return tilenum, tile


indexy = 0
try:
    while True:
        downside = bordertonum(latesttile[-1])
        downsidestr = latesttile[-1]
        while indexx >= 0:
            leftside = bordertonum(rotate(latesttile)[-1])
            leftsidestr = rotate(latesttile)[-1]
            print("looking left for", indexx, indexy, leftsidestr)
            tilenum, tile = findleft(tiles, leftside)
            latesttile = tile
            fillbigpicture(tile, indexx, indexy)
            printfloormap(tile)
            printfloormap(bigpicture)
            del tiles[tilenum]
            indexx -= 1

        indexx = sqrttiles - 1
        indexy += 1
        if indexy < sqrttiles:
            print("looking down for", indexx, indexy, downsidestr)
            tilenum, tile = finddown(tiles, downside)
            latesttile = tile
            fillbigpicture(tile, indexx, indexy)
            printfloormap(tile)
            printfloormap(bigpicture)
            del tiles[tilenum]
        indexx -= 1
except:
    pass


printfloormap(bigpicture)
printfloormap(cleanpicture)

seamonster = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]


def compare(line, monsterline):
    return all([j == " " or i == j for i, j in zip(line, monsterline)])


def findseamonsters(tile):
    counter = 0
    for i in range(len(tile) - 2):
        for j in range(len(tile[0]) - len(seamonster[0])):
            if all(
                (
                    compare(tile[i][j:], seamonster[0]),
                    compare(tile[i + 1][j:], seamonster[1]),
                    compare(tile[i + 2][j:], seamonster[2]),
                )
            ):
                print("found one at", j, i)
                counter += 1
    return counter


print("searching for monsters")
for orientation in getorientations(cleanpicture):
    if c := findseamonsters(orientation):
        printfloormap(orientation)
        print(c)
        break

roughness = 0
for line in cleanpicture:
    for char in line:
        if char == "#":
            roughness += 1
print(f"{roughness=}")
roughness -= 15 * c
print(f"{roughness=}")
