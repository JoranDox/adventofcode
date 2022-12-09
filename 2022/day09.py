
import pathlib
parent_directory = pathlib.Path(__file__).resolve().absolute().parent
# with open(parent_directory.joinpath("day09inputtest.txt")) as f:
# with open(parent_directory.joinpath("day09inputtest2.txt")) as f:
with open(parent_directory.joinpath("day09input.txt")) as f:
    data = f.read().strip()

def vsum(loc, dir):
    return tuple([i+j for i,j in zip(loc,dir)])
def vdiff(loc,dir):
    return tuple([i-j for i,j in zip(loc,dir)])
def vmul(loc, amt):
    return tuple([i*amt for i in loc])

# pos = [(0,0)]
# tpos = [(0,0)]
posses = []
# part 1: 2
# part 2: 10
for i in range(10):
    posses.append([(0,0)])

directions = {
    "U" : (0, -1),
    "R" : (1, 0),
    "D" : (0, 1),
    "L" : (-1, 0),
}
revdirections = {v:k for k,v in directions.items()}

# for i in range(5):
#     for j in range(5):
#         print(f"({i-2},{j-2}):")

tmoves = {
    (-2,-2): (-1, -1),
    (-2,-1): (-1, -1),
    (-2,0): (-1, 0),
    (-2,1): (-1, 1),
    (-2,2): (-1, 1),
    (-1,-2): (-1, -1),
    (-1,-1): (0,0),
    (-1,0): (0,0),
    (-1,1): (0,0),
    (-1,2): (-1, 1),
    (0,-2): (0, -1),
    (0,-1): (0,0),
    (0,0): (0,0),
    (0,1): (0,0),
    (0,2): (0, 1),
    (1,-2): (1, -1),
    (1,-1): (0,0),
    (1,0): (0,0),
    (1,1): (0,0),
    (1,2): (1, 1),
    (2,-2): (1, -1),
    (2,-1): (1, -1),
    (2,0): (1,0),
    (2,1): (1,1),
    (2,2): (1,1),
}

prevdir = None
for line in data.splitlines():
    # print(line)
    direction, amount = line.split()
    for i in range(int(amount)):
        for hindex in range(len(posses)-1):
            pos = posses[hindex]
            tpos = posses[hindex+1]
            # new position for head
            if hindex == 0:
                pos.append(vsum(pos[-1], directions[direction]))
            # print(pos)
            diff = vdiff(pos[-1], tpos[-1])
            # print(diff)
            difdir = tmoves[diff]
            # print(difdir)
            tpos.append(vsum(tpos[-1],difdir))
            # print(tpos)
            # print()
        # [
        #     print(p[-2:])
        #     for p in posses
        # ]
        # print()


print(len(set(posses[-1])))

# for line in data.split("\n\n"):


