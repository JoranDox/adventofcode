import numpy as np
import pathlib
import matplotlib.pyplot as plt

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day18inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day18input.txt")) as f:
    data = f.read().strip()

directions = {
    "U" : (0, -1),
    "L" : (-1, 0),
    "D" : (0, 1),
    "R" : (1, 0),
    # p2
    "0" : (1, 0),
    "1" : (0, 1),
    "2" : (-1, 0),
    "3" : (0, -1),
}
def inverse(direction):
    x,y = direction
    return (-x, -y)

def godirection(loc,direction,distance):
    x,y = loc
    return x + direction[0]*distance, y + direction[1]*distance

def mapprint(m):
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            if (x,y) in m:
                print("#", end=" ")
            else:
                print(" ", end=" ")
        print()

minx = 0
miny = 0
maxx = 0
maxy = 0
cur = (0,0)
locs = [cur]
edgelen = 0
plt.figure(figsize=(8, 8))
plt.axis('equal')
for line in data.splitlines():
    direction, distance, hexcolor = line.split()
    if True: # part 2 switch
        distance = int(hexcolor[2:-2], base=16)
        direction = hexcolor[-2]
    distance = int(distance)
    cur = godirection(cur, directions[direction], distance)
    plt.plot(*zip(locs[-1], cur), color=hexcolor[1:-1])
    edgelen += distance
    locs.append(cur)
    cx,cy = cur
    minx = min(minx,cx)
    miny = min(miny,cy)

    maxx = max(maxx,cx)
    maxy = max(maxy,cy)

# print(locs)
# mapprint(locs)

def PolyArea(x,y):
    # something something shoelace, just copied from stackoverflow
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

x,y = zip(*locs)
area = PolyArea(np.array(x),np.array(y))
print(area)

print(edgelen/2+1)
print(int(area) + (edgelen//2) + 1)


plt.fill(x, y)
plt.show()
