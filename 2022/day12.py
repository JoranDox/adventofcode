import collections
import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day12inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day12input.txt")) as f:
    data = f.read().strip()

seenlocs = {
    "p1": {},
    "p2": {},
}
tochecklocs = {
    "p1": [list() for i in range(len(data))],
    "p2": [list() for i in range(len(data))],
}
for y, line in enumerate(data.splitlines()):
    for x, char in enumerate(line):
        if char == "S":
            seenlocs["p1"][(x, y)] = 0
            tochecklocs["p1"][0].append(((x, y),))
            seenlocs["p2"][(x, y)] = 0
            tochecklocs["p2"][0].append(((x, y),))
        if char == "a":
            seenlocs["p2"][(x, y)] = 0
            tochecklocs["p2"][0].append(((x, y),))
        if char == "E":
            end = (x, y)

# print(seenlocs)
# print(tochecklocs)
data = data.replace("S", chr(ord("a")))
data = data.replace("E", chr(ord("z")))
# print("replaced S with", chr(ord("a")))
# print("replaced E with", chr(ord("z")))


def getneighbours(x, y):
    return (
        (x, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x, y + 1),
    )


themap = [[ord(l) for l in line] for line in data.splitlines()]


def tostr(themap):
    return "\n".join(["".join([chr(square) for square in line]) for line in themap])


def tostrend(themap, path):
    return "\n".join(
        [
            "".join(
                [
                    (chr(square) if ((sx, sy) in path) else ".")
                    for sx, square in enumerate(line)
                ]
            )
            for sy, line in enumerate(themap)
        ]
    )


def tostrseen(themap, part):
    return "\n".join(
        [
            "".join(
                [
                    (
                        str(seenlocs[part][(sx, sy)]).rjust(3)
                        if ((sx, sy) in seenlocs[part])
                        else "..."
                    )
                    for sx, square in enumerate(line)
                ]
            )
            for sy, line in enumerate(themap)
        ]
    )


# print(tostr(themap))


class Hat(Exception):
    # raise your hat when you're done
    pass


for part in "p1", "p2":
    try:
        iterations = 0
        while any(tochecklocs[part]):
            for steps, sublist in enumerate(tochecklocs[part]):
                # print("steps:", steps)
                if sublist:
                    path_to_here = sublist.pop()
                    # print(path_to_here)
                    assert steps == len(path_to_here) - 1
                    x, y = path_to_here[-1]
                    currpos = themap[y][x]
                    # print("at", x, y, currpos)
                    iterations += 1
                    newseen = False
                    for nx, ny in getneighbours(x, y):
                        # print("checking", nx, ny, end=" ")
                        if (
                            nx < 0
                            or ny < 0
                            or nx >= len(themap[0])
                            or ny >= len(themap)
                        ):
                            # print("\nnot on map")
                            continue
                        neigh = themap[ny][nx]
                        # print("neigh", neigh)
                        if neigh <= (currpos + 1):
                            if (nx, ny) == end:
                                print(part + ":", len(path_to_here))
                                # print(path_to_here + ((nx,ny),))
                                # print(" ".join(str(themap[ky][kx]) for kx,ky in path_to_here + ((nx,ny),)))
                                # print("".join(chr(themap[ky][kx]) for kx,ky in path_to_here + ((nx,ny),)))
                                print(tostrend(themap, path_to_here + ((nx, ny),)))
                                # print(tostrseen(themap, part))
                                raise Hat()
                            # print("okay")
                            if (nx, ny) in seenlocs[part]:
                                if (
                                    seenlocs[part][(nx, ny)] > steps + 1
                                    and part == "p1"
                                ):
                                    print(
                                        "this shouldn't happen in p1",
                                        (nx, ny),
                                        "already seen with:",
                                        seenlocs[part][(nx, ny)],
                                        "but now I got here in",
                                        steps + 1,
                                    )
                                # print("already seen as", seenlocs[part][(nx,ny)])
                            if ((nx, ny) not in seenlocs[part]) or (
                                seenlocs[part][(nx, ny)] > steps + 1
                            ):
                                # print("yes")
                                newseen = True
                                seenlocs[part][(nx, ny)] = steps + 1
                                # check em (again)
                                tochecklocs[part][steps + 1].append(
                                    path_to_here + ((nx, ny),)
                                )
                    # if not (iterations % 100):
                    #     print(iterations,tochecklocs[part])
                    if newseen:
                        # print(seenlocs[part])
                        # print("new neighbours,")
                        break  # jump to while loop
    except Hat:
        pass
