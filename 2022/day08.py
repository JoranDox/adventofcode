
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
#with open(aoc_dir.joinpath("input/2022/day08inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day08input.txt")) as f:
    data = f.read().strip()

treemap = []
vismap = []
vm2 = []
for line in data.splitlines():
    treemap.append([int(i) for i in line])
    vismap.append([set() for i in line])
    vm2.append([False for i in line])

def mprint(treemap):
    return "\n".join([
        ("".join((str(i) for i in line)))
        for line in treemap
    ])
print(mprint(treemap))
print(vismap)
directions = {
    "n" : (0, -1),
    "e" : (1, 0),
    "s" : (0, 1),
    "w" : (-1, 0),
}
inv_dirs = {
    "n": "s",
    "e": "w",
    "s": "n",
    "w": "e",
}
def vsum(loc, dir):
    return tuple([i+j for i,j in zip(loc,dir)])

print(vsum((2,5), (3,9)))

for y,line in enumerate(vm2):
    # print(y, line)
    for x,visibilities in enumerate(line):
        # print(x,visibilities)
        for direction in {"n","e","s","w"}:
            cx,cy = vsum((x,y), directions[direction])
            if (cy < 0) or (cx < 0) or (cx >= len(vismap[0])) or (cy >= len(vismap)):
                vm2[y][x] = True
                continue

        if vm2[y][x]:
            continue

        colvals = [i[x] for i in treemap]
        rowvals = treemap[y]
        myval = treemap[y][x]
        if (
            (max(colvals[:y]) < myval)
            or (max(colvals[y+1:]) < myval)
            or (max(rowvals[:x]) < myval)
            or (max(rowvals[x+1:]) < myval)
        ):
            vm2[y][x] = True




print(mprint(vm2))
counter = 0
for line in vm2:
    for vis in line:
        if vis:
            counter += 1
print("p1:", counter)

highscore = 0

def getscore(array):
    try:
        return array.index(False) + 1
    except:
        return len(array)

def getscenicscore(x,y):
    # x,y = 2,3
    # print(treemap[y][x])
    colvals = [i[x] for i in treemap]
    # print(colvals)
    rowvals = treemap[y]
    # print(rowvals)
    myval = treemap[y][x]
    # up
    # print([i < myval for i in (colvals[:y])][::-1])
    # left
    # print([i < myval for i in (rowvals[:x])][::-1])
    # down
    # print([i < myval for i in (colvals[y+1:])])
    # right
    # print([i < myval for i in (rowvals[x+1:])])

    return (
        (getscore([i < myval for i in (colvals[:y])][::-1]))
        *(getscore([i < myval for i in (rowvals[:x])][::-1]))
        *(getscore([i < myval for i in (colvals[y+1:])]))
        *(getscore([i < myval for i in (rowvals[x+1:])]))
    )


    # return [
    #     (getscore([i < myval for i in (colvals[:y])][::-1])),
    #     (getscore([i < myval for i in (rowvals[:x])][::-1])),
    #     (getscore([i < myval for i in (colvals[y+1:])])),
    #     (getscore([i < myval for i in (rowvals[x+1:])])),
    # ]



# print(getscenicscore(2,3))

for y,line in enumerate(vm2):
    for x,visibilities in enumerate(line):
        scores = getscenicscore(x,y)

                    #  (max(colvals[y+1:]) < myval)
                    # or (max(rowvals[:x]) < myval)
                    # or (max(rowvals[x+1:]) < myval)
        if scores > highscore:
            highscore = scores
            print(scores)