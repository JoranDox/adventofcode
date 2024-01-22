import pathlib
import tqdm
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day22inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day22input.txt")) as f:
    data = f.read().strip()

bricks = []
minz = 1000000
for line in tqdm.tqdm(data.splitlines()):
    brickstart, brickend = [
        tuple([int(pos) for pos in brick.split(",")]) for brick in line.split("~")
    ]
    # print(brickstart, brickend)
    minz = min(minz, brickstart[2], brickend[2])
    if brickstart == brickend:
        bricks.append({brickstart})
    else:
        for dim in range(3):
            if brickstart[dim] != brickend[dim]:
                mn = min(brickstart[dim], brickend[dim])
                mx = max(brickstart[dim], brickend[dim])
                bricks.append({
                    (
                        brickstart[0] if dim != 0 else brickcur,
                        brickstart[1] if dim != 1 else brickcur,
                        brickstart[2] if dim != 2 else brickcur,
                    ) for brickcur in range(mn, mx+1)
                })

    # print(bricks)
print(len(bricks))
print("minz", minz)
def cubelow(cube: tuple[int]):
    return (*cube[:2], cube[2]-1)

def below(brick:frozenset[tuple[int]]):
    return {
        cubelow(cube) for cube in brick
    }


# def supportedby(index: int):
#     return i for i in

def legalbelow(index:int, bricks: list[frozenset[tuple[int]]]) -> tuple[bool, frozenset[tuple[int]]] :
    b = below(bricks[index])
    if any(cube[2] < minz for cube in b):
        # too low
        return False, tuple()
    cubes_without_faller = {
        cube
        for i, brick in enumerate(bricks) if i != index
        for cube in brick
    }
    if cubes_without_faller & b:
        # overlap with existing cube, can't fall
        return False, (cubes_without_faller & b) # bricks that are supporting the given brick
    return True, b # this brick, one lower

allcubes = {
    cube
    for i, brick in enumerate(bricks)
    for cube in brick
}
b = bricks[0]
cwf = {
    cube
    for i, brick in enumerate(bricks) if i != 0
    for cube in brick
}

def makeeverythingfall(bricks):
    changed = True
    fell = [False for _ in bricks]
    while changed:
        changed = False
        for i in range(len(bricks)):
            legal, lb = legalbelow(i, bricks)
            if legal:
                bricks[i] = lb
                changed = True
                fell[i] = True
    return bricks, sum(fell)

bricks, fell = makeeverythingfall(bricks)
print("bricks", bricks)
print("and", fell, "fell")

# potential = [0 for _ in bricks]
felllist = [0 for _ in bricks]
for i, brick in tqdm.tqdm(enumerate(bricks)):
    # leave one out
    tempbricks = bricks[:i] + bricks[i+1:]
    assert brick not in tempbricks

    # check if anything falls
    _, fell = makeeverythingfall(tempbricks)
    felllist[i] = fell

    # for index in range(len(tempbricks)):
    #     legal, _ = legalbelow(index, tempbricks)
    #     if legal:
    #         potential[i] += 1
    #         # todo p2 recursive this

# print(potential)
print(felllist)
print("p1:", len([p for p in felllist if not p]))



print("p2:", sum(felllist))
