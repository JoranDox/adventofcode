
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2025/day12inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2025/day12input.txt")) as f:
    data = f.read().strip()

# all blocks are 3x3, and except for one, all have a # in the center
block = tuple[tuple[int,...],...]

class Area:
    hsize: int
    vsize: int
    blockcounts: list[int]

blocks: list[block] = []
areas: list[Area] = []
for i, datablock in enumerate(data.split("\n\n")):
    blockdata = datablock.splitlines()
    if blockdata[0].strip() == f"{i}:":
        # it's a real block

        assert len(blockdata) == 4
        for line in blockdata[1:]:
            assert len(line) == 3

        blocks.append(tuple(
            tuple(1 if c == "#" else 0 for c in line)
            for line in blockdata[1:]
        ))
    else:
        # it's the rest of the instructions
        for line in blockdata:
            sizes, blockcountstr = line.split(": ")
            hsizestr, vsizestr = sizes.split("x")
            area = Area()
            area.hsize = int(hsizestr)
            area.vsize = int(vsizestr)
            area.blockcounts = [int(x) for x in blockcountstr.split()]
            areas.append(area)

blockminsize = [sum(sum(row) for row in b) for b in blocks]
fillable = 0
maybefillable = 0
for area in areas:
    areasize = area.hsize * area.vsize
    neededsize = 0
    maxsize = 0
    for blocksize, needed in zip(area.blockcounts, blockminsize):
        neededsize += blocksize * needed
        maxsize += blocksize * 9

    if neededsize > areasize:
        print("Area too small")
    elif areasize >= maxsize:
        print("Area always fillable")
        fillable += 1
    else:
        print("Area maybe fillable")
        maybefillable += 1
print(f"Number of fillable areas: {fillable}, maybe fillable areas: {maybefillable}")

"""

###
##.
##.

##.
###
##.

###
#..
###

###
#..
###

###
#..
###

###
.#.
###

###
.#.
###

"""