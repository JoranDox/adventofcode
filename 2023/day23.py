import collections
import queue
import heapq
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2023/day23inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2023/day23input.txt")) as f:
    data = f.read().strip()


downhillmap = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}
trailmap = {}
start = None
finish = None
for y, line in enumerate(data.splitlines()):
    for x, char in enumerate(line):
        trailmap[x,y] = char
        if char != "#":
            finish = (x,y)
            if start is None:
                start = (x,y)
maxx = x
maxy = y

print(start, finish, maxx, maxy)

def legal(x,y):
    if x < 0 or y < 0 or x > maxx or y > maxy or trailmap[x,y] == "#":
        return False
    return True

def neighbours(x,y, p1=True):
    char = trailmap[x,y]
    if char in downhillmap and p1:
        return [(x + downhillmap[char][0], y + downhillmap[char][1])]
    else:
        return [
            (xx, yy) for (xx,yy) in (
                (x-1, y),
                (x, y-1),
                (x+1, y),
                (x, y+1),
            )
            if legal(xx,yy)
        ]

print(neighbours(*start))

def printpath(path):
    for y in range(maxy+1):
        for x in range(maxx+1):
            if (x,y) in path:
                print("O", end='')
            else:
                print(trailmap[x,y],end='')
        print()

best_finish = 0
todo = collections.deque()
todo.append((start,))
while todo:
    path = todo.popleft()
    for n in neighbours(*path[-1]):
        if n not in path:
            if n == finish:
                # printpath(path + (n,))
                if len(path) > best_finish:
                    print(len(path))
                    best_finish = len(path)
            else:
                todo.append(path + (n,))

print("p1:", best_finish)


# todo = collections.deque()
# TODO: maybe check whether we've been in a location with a longer path first? but that doesn't seem stable
todo = []
seen = {start: 1}
heapq.heappush(todo, (1, (start,)))
while todo:
    _, path = heapq.heappop(todo)
    # print(path)
    for n in neighbours(*path[-1], p1=False):
        if n not in path:
            if n == finish:
                # printpath(path + (n,))
                if len(path) > best_finish:
                    print(len(path))
                    best_finish = len(path)
                    printpath(path + (n,))

            else:
                if n not in seen or len(path) > seen[n]:
                    heapq.heappush(todo, (sum(n) - len(path), path + (n,)))
                    seen[n] = len(path)


print("p2:", best_finish)

# tried: 5854, 5886, 6xxx
# legal tiles: 9173