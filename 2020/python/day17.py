
infilename = "day17input.txt"
# infilename = "day17inputex.txt"


dddfloormap = []

floormap = []
floorset = set()
with open(infilename) as infile:
    w = 0
    z = 0
    for y, line in enumerate(infile):
        for x, char in enumerate(line.strip()):
            if char == "#":
                floorset |= {(w, z, y, x)}
        floormap.append(
            [char for char in line.strip()]
        )
print(floorset)
dddfloormap.append(floormap)

def print3dfloormap(floormap):
    for z, layer in enumerate(floormap):
        print(f"{z=}")
        printfloormap(layer)
def printfloormap(floormap):
    # print(floormap)
    print("\n".join("".join(line) for line in floormap))
    print()

def printfloorset(floorset):
    maxz = maxy = maxx = -1000
    minz = miny = minx = 1000

    for z,y,x in floorset:
        maxz = max(maxz, z)
        maxy = max(maxy, y)
        maxx = max(maxx, x)
        minz = min(minz, z)
        miny = min(miny, y)
        minx = min(minx, x)
    # print(f"{minz=}{miny=}{minx=}")
    # print(f"{maxz=}{maxy=}{maxx=}")
    temp3dfloormap = []
    for z in range(minz, maxz+1):
        ztemp = []
        for y in range(miny, maxy+1):
            ytemp = []
            for x in range(minx, maxx+1):
                ytemp.append(".")
            ztemp.append(ytemp)
        temp3dfloormap.append(ztemp)
        
    print3dfloormap(temp3dfloormap)

    # print(floorset)

    for z,y,x in floorset:
        # print(f"{z=}{y=}{x=}")
        # print(f"{z - minz}{y - miny}{x - minx}")
        temp3dfloormap[z - minz][y - miny][x - minx] = "#"
    print3dfloormap(temp3dfloormap)

# printfloormap(floormap)
# print3dfloormap(dddfloormap)
# printfloorset(floorset)

def getneighbourcoords(coords):
    # print(f'{coords=}')
    samplecoords = {coords}
    for i in range(len(coords)):
        newsamplecoords = {*samplecoords}
        for temp in samplecoords:
            # print(f"{temp}")
            newsamplecoords |= {
                (*(temp[:i]), temp[i]+1, *(temp[i+1:])),
                (*(temp[:i]), temp[i]-1, *(temp[i+1:]))
            }
        samplecoords = newsamplecoords
        # print(samplecoords)
    samplecoords ^= {coords} # remove original
    # print(samplecoords)
    return samplecoords

# print(getneighbourcoords((1,1, 1)))

def cycle(floorset):
    newfloorset = set()
    for coords in floorset:
        for neighbour in getneighbourcoords(coords):
            activeneighbours = sum(1 for x in getneighbourcoords(neighbour) if x in floorset)
            if activeneighbours == 3:
                newfloorset |= {neighbour}
            elif activeneighbours == 2 and neighbour in floorset:
                newfloorset |= {neighbour}
    return newfloorset

print("start")
for i in range(6):
    # printfloorset(floorset)
    floorset = cycle(floorset)
    print("count:", len(floorset))




# def getneighbours(floormap, coords):
#     """
#     coords is an iterable set of coordinates like (x, y) or (x, y, z) or the like
#     """
#     ret = []
#     samplecoords = []
#     for i, coord in enumerate(coords):
#         samplecoords = [
#             coord[]
#         ]
#     for ydiff in range(-1, 2):
#         for xdiff in range(-1, 2):
#             if ydiff == xdiff == 0:
#                 continue
#             tempx = x+xdiff
#             tempy = y+ydiff
#             neighbour = mapget(floormap, tempx, tempy)
#             # print(f"{neighbour=}")
#             if seeing:
#                 while neighbour is not None and neighbour == ".":
#                     tempx += xdiff
#                     tempy += ydiff
#                     neighbour = mapget(floormap, tempx, tempy)
                
#             if neighbour is not None:
#                 # print("appending")

#                 ret.append(neighbour)
#     return ret
    
# def change(seat, neighbours):
#     if seat == "L" and "#" not in neighbours:
#         # print("get full:", seat, neighbours)
#         return "#"
#     if seat == "#" and sum(1 for x in neighbours if x == "#") >= tolerance:
#         # print("get empty:", seat, neighbours)
#         return "L"
#     # print("same:", seat, neighbours)
#     return seat

# def nextstep(floormap):
#     newmap = []
#     for y in range(ymax):
#         templst = []
#         for x in range(xmax):
            
#             tempval = change(mapget(floormap, x, y), getneighbours(floormap, x, y))

#             templst.append(tempval)
#         newmap.append(templst)
#     return newmap


# curr = floormap
# last = None
# while curr != last:
#     last = curr
#     printfloormap(curr := nextstep(curr))
# printfloormap(curr)
# print(
#     sum(
#         (
#             sum(1 for y in line if y == "#")
#         )
#         for line in curr    
#     )
# )