
with open("day20inputtest.txt") as f:
# with open("day20input.txt") as f:
    data = f.read().strip()

enhancer, image = data.split('\n\n')

dots = set()
for y,line in enumerate(image.splitlines()):
    for x,val in enumerate(line):
        if val == '#':
            dots.add((x,y))
print(dots)

image = [[l == "#" for l in line.strip()] for line in image]

def reduce(image):
    while not any(image[0]):
        image = image[1:]
    while not any(image[-1]):
        image = image[:-1]
    while not any(l[0] for l in image):
        image = [l[1:] for l in image]
    while not any(l[-1] for l in image):
        image = [l[:-1] for l in image]

def getbounds(dots):
    minx = 0
    miny = 0
    maxx = 0
    maxy = 0
    for x,y in dots:
        minx = min(minx, x)
        miny = min(miny, y)
        maxx = max(maxx, x)
        maxy = max(maxy, y)
    return  minx, maxx, miny, maxy

print(getbounds(dots))

def getneighbours(x,y):
    return (
        (x-1, y-1),
        (x,   y-1),
        (x+1, y-1),
        (x-1, y),
        (x,y),
        (x+1, y),
        (x-1, y+1),
        (x, y+1),
        (x+1, y+1),
    )

def getnumi(image, loc, beyond=False):
    maxx = len(image[0])
    maxy = len(image)
    l = 0
    for x,y in getneighbours(*loc):
        l *= 2
        if 0 < x < maxx and 0 < y < maxy:
            l += image[y][x]
        else:
            l += beyond
    return l

def getnum(dots, loc, beyond=False):
    minx, maxx, miny, maxy = getbounds(dots)
    l = 0
    for x,y in getneighbours(*loc):
        l *= 2
        if minx < x < maxx and miny < y < maxy:
            l += (x,y) in dots
        else:
            l += beyond
    return l
    return int("".join(
        str(int((i,j) in dots))
        for i,j in getneighbours(*loc)
    ),2)

print(getnum(dots, (2,2)))
print(getnum(dots, (0,0)))
print(getnum(dots, (0,0), 1))
print(int("111100100",2))

def enhance(imagedots, enhancer, beyond='.'):
    todo = set()
    for dot in imagedots:
        todo |= set(getneighbours(*dot))
    # print(todo)
    return {
        loc
        for loc in todo
        if (enhancer[getnum(imagedots, loc, beyond=='#')] == '#')
    }

def enhanceinversetwice(imagedots, enhancer):
    todo = set()
    for dot in imagedots:
        todo |= set(getneighbours(*dot))
    # print(todo)
    stilloff = {
        loc
        for loc in todo
        if not (enhancer[getnum(imagedots, loc, beyond=='#')] == '#')
    }




once = enhance(dots, enhancer, beyond='.')
twice = enhance(once, enhancer, beyond='.')

def toimage(dots):
    minx, maxx, miny, maxy = getbounds(dots)
    dots = {(x - minx, y - miny) for x,y in dots}
    print(dots, maxx, maxy)
    maxx -= minx
    maxy -= miny
    import numpy as np
    image = np.zeros((maxy+1, maxx+1), int)
    for x,y in dots:
        image[y][x] = 1
    print(image)
    for line in image:
        print("".join([("  ", "██")[l] for l in line]))
# toimage(dots)
# toimage(once)
# toimage(twice)


print(len(once))
print(len(twice))

# not 5440 -> too low