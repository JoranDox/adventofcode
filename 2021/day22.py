import tqdm
import logging

logging.basicConfig()

logger = logging.getLogger()

# with open("day22inputtestsmall.txt") as f:
# with open("day22inputtest.txt") as f:
with open("day22input.txt") as f:
    data = f.read().strip()

steps = []
# bounds = range(-50,50)
minx, maxx = -50, 50
ons = set()


def rangeincl(r):
    return range(r[0], r[1] + 1)


def rangeoverlap(r1, r2):
    return (max(r1[0], r2[0]), min(r1[1], r2[1]))


logger.debug(rangeoverlap((1, 5), (1, 10)))
logger.debug(rangeincl(rangeoverlap((1, 5), (1, 10))))
logger.debug(len(rangeincl(rangeoverlap((1, 5), (1, 10)))))


def cubeoverlap(c1, c2):
    return tuple(rangeoverlap(dim1, dim2) for dim1, dim2 in zip(c1, c2))


ctest1 = ((10, 12), (10, 12), (10, 12))
ctest2 = ((10, 12), (10, 11), (10, 12))
logger.debug(cubeoverlap(ctest1, ctest2))


def cubesize(cube):
    r = 1
    for c in cube:
        r *= len(rangeincl(c))
    return r


logger.debug(cubesize(ctest1))
logger.debug(cubesize(ctest2))


def splitrange(r1, r2):
    # returns 3 ranges:
    # r1 left of r2, r1 intersect r2, r1 right of r2
    start, end = r1
    scomp, ecomp = r2

    s0, s1, s2, s3 = sorted([*r1, *r2])

    overlap = (s1, s2) if s1 in rangeincl(r2) and s2 in rangeincl(r2) else None
    if not overlap:
        left = (s0, s1) if scomp > start else None
        right = (s2, s3) if ecomp < end else None
    else:
        left = (s0, s1 - 1) if scomp > start else None
        right = (s2 + 1, s3) if ecomp < end else None

    return (
        left,
        overlap,
        right,
    )


def testeq(a, b):
    assert a == b, f"{a} is not {b}"


testeq(splitrange((1, 3), (2, 4)), ((1, 1), (2, 3), None))
testeq(splitrange((2, 4), (1, 3)), (None, (2, 3), (4, 4)))
testeq(splitrange((2, 3), (1, 4)), (None, (2, 3), None))
testeq(splitrange((1, 4), (2, 3)), ((1, 1), (2, 3), (4, 4)))
testeq(splitrange((1, 2), (3, 4)), ((1, 2), None, None))
testeq(splitrange((3, 4), (1, 2)), (None, None, (3, 4)))

testeq(splitrange((1, 3), (1, 4)), (None, (1, 3), None))
testeq(splitrange((1, 4), (1, 3)), (None, (1, 3), (4, 4)))

testeq(splitrange((2, 3), (1, 3)), (None, (2, 3), None))
testeq(splitrange((1, 3), (2, 3)), ((1, 1), (2, 3), None))


def splitcube(c1, c2):
    one = []
    overlap = []
    two = []
    tocheck = {((), (c1, c2))}
    iters = 0
    while tocheck:
        logger.debug("iter", iters)
        iters += 1
        prefix, (c1, c2) = tocheck.pop()
        logger.debug(prefix, (c1, c2))
        i = len(prefix)
        logger.debug("i", i)
        rangea, postfixa = c1[0], c1[1:]
        rangeb, postfixb = c2[0], c2[1:]
        logger.debug("ranges")
        logger.debug(rangea)
        logger.debug(rangeb)
        o1, o2, o3 = splitrange(rangea, rangeb)
        logger.debug(o1, o2, o3)
        t1, t2, t3 = splitrange(rangeb, rangea)
        logger.debug(t1, t2, t3)
        overlapped = False
        if o1:
            logger.debug("one before")
            one.append((*prefix, o1, *postfixa))
        if o2:
            logger.debug("one overlap")
            # overlap: go deeper
            overlapped = ((*prefix, o2), (postfixa, postfixb))
            logger.debug(i, len(c1))
            if postfixa:
                tocheck.add(overlapped)
            else:
                overlap.append((*prefix, o2))
        if o3:
            logger.debug("one after")
            one.append((*prefix, o3, *postfixa))
        if t1:
            logger.debug("two before")
            two.append((*prefix, t1, *postfixb))
        if t2:
            logger.debug("two overlap")
            # overlap: they should be the same
            assert overlapped == ((*prefix, t2), (postfixa, postfixb))
        if t3:
            logger.debug("two after")
            two.append((*prefix, t3, *postfixb))
    return (
        one,
        overlap,
        two,
    )


logger.debug(splitrange((1, 3), (2, 4)))
logger.debug("split")

# lines
testeq(
    splitcube(((1, 3),), ((2, 4),)),
    (
        [((1, 1),)],  # only for 1
        [((2, 3),)],  # overlaps
        [((4, 4),)],  # only for 2
    ),
)

# squares
testeq(
    splitcube(((1, 3), (1, 3)), ((2, 4), (2, 4))),
    (
        [((1, 1), (1, 3)), ((2, 3), (1, 1))],
        [((2, 3), (2, 3))],
        [((4, 4), (2, 4)), ((2, 3), (4, 4))],
    ),
)
# cubes
testeq(
    splitcube(((1, 3), (1, 3), (1, 3)), ((2, 4), (2, 4), (2, 4))),
    (
        [((1, 1), (1, 3), (1, 3)), ((2, 3), (1, 1), (1, 3)), ((2, 3), (2, 3), (1, 1))],
        [((2, 3), (2, 3), (2, 3))],
        [((4, 4), (2, 4), (2, 4)), ((2, 3), (4, 4), (2, 4)), ((2, 3), (2, 3), (4, 4))],
    ),
)
# cubes, no overlap
testeq(
    splitcube(((1, 3), (1, 3), (1, 2)), ((2, 4), (2, 4), (3, 4)))[1],
    [],
)
# cubes, 1 is in 2
testeq(
    splitcube(((2, 2), (2, 2), (2, 2)), ((2, 4), (2, 4), (2, 4)))[0],
    [],
)
# cubes, 2 is in 1
testeq(
    splitcube(((2, 4), (2, 4), (2, 4)), ((2, 2), (2, 2), (2, 2)))[2],
    [],
)
# (
#     [((1, 1), (1, 3), (1, 2)), ((2, 3), (1, 1), (1, 2)), ((2, 3), (2, 3), (1, 2))],
#     [],
#     [((4, 4), (2, 4), (3, 4)), ((2, 3), (4, 4), (3, 4)), ((2, 3), (2, 3), (3, 4))]
# ) is not (
#     [((1, 1), (1, 3), (1, 2)), ((2, 3), (1, 1), (1, 2)), ((2, 3), (2, 3), (1, 2))],
#     [],
#     [((4, 4), (2, 4), (2, 4)), ((2, 3), (4, 4), (2, 4)), ((2, 3), (2, 3), (4, 4))]
# )
cubes = []
maxoverlap = 0
for line in tqdm.tqdm(data.splitlines()):
    onoff, coords = line.strip().split(" ")

    xrange, yrange, zrange = [
        tuple(map(int, coord.split("=")[1].split(".."))) for coord in coords.split(",")
    ]
    cubes.append((onoff, (xrange, yrange, zrange)))
    overlaps = 0
    for onoff, cube in cubes:
        if cubesize(cubeoverlap(cube, (xrange, yrange, zrange))):
            overlaps += 1

        maxoverlap = max(overlaps, maxoverlap)
    logger.debug(overlaps)
logger.debug("max overlaps", maxoverlap)
print(len(cubes), "cubes")
# part 1
for onoff, (xrange, yrange, zrange) in tqdm.tqdm(cubes):
    # logger.debug(onoff, coords)

    if (
        xrange[0] > maxx
        or xrange[1] < minx
        or yrange[0] > maxx
        or yrange[1] < minx
        or zrange[0] > maxx
        or zrange[1] < minx
    ):
        # logger.debug('out of bounds, skip')
        continue

    xrange = (max(xrange[0], minx), min(xrange[1], maxx))
    yrange = (max(yrange[0], minx), min(yrange[1], maxx))
    zrange = (max(zrange[0], minx), min(zrange[1], maxx))
    logger.debug(xrange, yrange, zrange)

    subset = {
        (x, y, z)
        for x in rangeincl(xrange)
        for y in rangeincl(yrange)
        for z in rangeincl(zrange)
    }
    logger.debug(onoff, len(subset))
    assert cubesize((xrange, yrange, zrange)) == len(subset), cubesize(
        (xrange, yrange, zrange)
    ) == len(subset)
    assert onoff in ("on", "off")
    if onoff == "on":
        ons |= subset
    elif onoff == "off":
        ons -= subset
    # break


print("part 1", len(ons))

# part 2
oncubes = {}

for onoff, newcube in tqdm.tqdm(cubes):
    newoncubes = set()
    tocheckcubes = set()
    for cube in oncubes:
        if cubesize(cubeoverlap(cube, newcube)):
            one, overlap, two = splitcube(cube, newcube)
            if onoff == "on":
                newoncubes |= {*one, newcube}
            else:
                newoncubes |= set(one)
                # just don't add the overlap & two part
        else:
            newoncubes.add(cube)
    if onoff == "on":
        newoncubes.add(newcube)
    # print(len(newoncubes), sum(cubesize(c) for c in newoncubes))
    oncubes = newoncubes
print(len(oncubes), sum(cubesize(c) for c in oncubes))
