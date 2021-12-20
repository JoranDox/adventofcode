import numpy as np
import tqdm

# with open("day20inputtest.txt") as f:
with open("day20input.txt") as f:
    data = f.read().strip()

enhancer, image = data.split("\n\n")
enhancer_bin = [int(e == "#") for e in enhancer.strip()]
dots = set()
for y, line in enumerate(image.splitlines()):
    for x, val in enumerate(line):
        if val == "#":
            dots.add((x, y))
print(dots)

# we can rebuild densely
print(repr(image))
image = [[int(l == "#") for l in line.strip()] for line in image.splitlines()]
print(image)
image = np.array(image)
print("np\n", image)


def getbounds(dots):
    minx = 0
    miny = 0
    maxx = 0
    maxy = 0
    for x, y in dots:
        minx = min(minx, x)
        miny = min(miny, y)
        maxx = max(maxx, x)
        maxy = max(maxy, y)
    return minx, maxx, miny, maxy


print(getbounds(dots))


def getneighbours(x, y):
    return (
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    )


def getnumd(image, loc, beyond=0):
    # dense
    maxx = len(image[0])
    maxy = len(image)
    assert maxx == image.shape[1]
    assert maxy == image.shape[0]
    maxx, maxy = image.shape

    l = 0
    for x, y in getneighbours(*loc):
        l *= 2
        if 0 <= x < maxx and 0 <= y < maxy:
            l += image[y][x]
        else:
            l += beyond
    return l


def getnums(dots, loc):
    # sparse
    # minx, maxx, miny, maxy = getbounds(dots)
    # l = 0
    # for x, y in getneighbours(*loc):
    #     l *= 2
    #     if minx < x < maxx and miny < y < maxy:
    #         l += (x, y) in dots
    #     else:
    #         l += beyond
    # return l
    return int("".join(str(int((i, j) in dots)) for i, j in getneighbours(*loc)), 2)


# print("nums", getnums(dots, (2, 2)))
# print("numd", getnumd(image, (2, 2)))
for y in range(-2, 7):
    for x in range(-2, 7):
        nums = getnums(dots, (x, y))
        numd = getnumd(image, (x, y))
        assert nums == numd, (x, y, nums, numd)

nums = getnums(dots, (x, y))
numd = getnumd(image, (x, y))

# for y in 1,2,3:
#     print(image[y][1:4])

# print("nums", getnums(dots, (-1, -1)))
# print("numd", getnumd(image, (-1, -1)))

# print(int("111100100",2))


def enhances(imagedots, enhancer):
    todo = set()
    for dot in imagedots:
        todo |= set(getneighbours(*dot))
    # print(todo)
    return {loc for loc in todo if (enhancer[getnums(imagedots, loc)] == "#")}


def enhanced(image, enhancer, beyond=0):
    # image: 2d array of 0 or 1
    # enhancer: 1d array of 0 or 1
    # beyond: what to expect out of the bounds of the image
    newbeyond = enhancer[0] ^ beyond

    newimg = []
    bigbounds = 2
    for y in range(len(image) + 2 * bigbounds):  # y = -1 ..
        newline = []
        for x in range(len(image[0]) + 2 * bigbounds):
            # extra big bounds => decrease x & y by half bounds to compensate
            newnum = getnumd(image, (x - bigbounds, y - bigbounds), beyond=beyond)
            newval = enhancer[newnum]
            newline.append(newval)
        newimg.append(newline)
    return np.array(newimg), newbeyond


def toimaged(image, beyond=0):
    # print(image)
    for line in np.pad(image, 1, mode="constant", constant_values=beyond):
        # for line in image:
        print("".join([("  ", "██")[l] for l in line]))
    print()


def toimages(dots):
    minx, maxx, miny, maxy = getbounds(dots)
    dots = {(x - minx, y - miny) for x, y in dots}
    # print(dots, maxx, maxy)
    maxx -= minx
    maxy -= miny
    image = np.zeros((maxy + 1, maxx + 1), int)
    for x, y in dots:
        image[y][x] = 1
    toimaged(image)


def reduceonce(image, beyond):
    if all(image[0] == beyond):
        return image[1:]

    if all(image[-1] == beyond):
        return image[:-1]

    if all(image[:, 0] == beyond):
        return image[:, 1:]

    if all(image[:, -1] == beyond):
        return image[:, :-1]


def reduce(image, beyond=0):
    c = reduceonce(image, beyond)
    while c is not None:
        image = c
        # toimaged(image)
        c = reduceonce(image, beyond)
    return image


print("start")
toimaged(image)

print("once")
onced, newbeyond = enhanced(image, enhancer_bin, beyond=0)
print(f"{newbeyond=}")
toimaged(reduce(onced, beyond=newbeyond), beyond=newbeyond)

print("twice")
twiced, newbeyond = enhanced(onced, enhancer_bin, beyond=newbeyond)
print(f"{newbeyond=}")
toimaged(reduce(twiced, beyond=newbeyond), beyond=newbeyond)


# print(len(once))
# print(len(twice))
print(np.core.numeric.count_nonzero(twiced))
newimg = twiced
for i in tqdm.tqdm(range(48)):
    newimg, newbeyond = enhanced(newimg, enhancer_bin, beyond=newbeyond)
print(np.core.numeric.count_nonzero(newimg))
# not 5440 -> too low
