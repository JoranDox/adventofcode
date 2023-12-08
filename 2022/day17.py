import collections
import copy
import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day17inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day17input.txt")) as f:
    jet = f.read().strip()

rocks = [
    [
        "####",
    ],
    [
        " # ",
        "###",
        " # ",
    ],
    [
        "  #",
        "  #",
        "###",
    ],
    [
        "#",
        "#",
        "#",
        "#",
    ],
    [
        "##",
        "##",
    ],
]

map = collections.defaultdict(lambda: [" " for i in range(7)])
map[0] = "-------"


def printmap(map, topx=None):
    if topx is None:
        for y in range(max(map) + 1, start - 1, -1):
            print("|" + "".join(map[y]) + "|")
        print()
    else:
        for y in range(max(map) + 1, max(map) + 1 - topx, -1):
            print("|" + "".join(map[y]) + "|")
        print()


def putonmap(map, rock, pos):
    x, y = pos
    for ry, rrow in enumerate(rock[::-1]):
        for rx, r in enumerate(rrow):
            assert r == " " or map[y + ry][x + rx] == " "
            if r != " ":
                map[y + ry][x + rx] = r


def printmapwithrock(map, rock, pos):
    m2 = copy.deepcopy(map)
    putonmap(m2, rock, pos)
    printmap(m2)


def check_collision(map, rock, pos):
    x, y = pos
    # wall collision
    for rx in range(len(rock[0])):
        if not (0 <= x + rx < 7):
            return True  # yes collision

    for ry, rrow in enumerate(rock[::-1]):
        for rx, r in enumerate(rrow):
            # other block collision
            if r != " " and map[y + ry][x + rx] != " ":
                return True
    return False


def get_start(map):
    x = 2

    y = max(map)
    while map[y] == map[-1]:
        y -= 1
    return (x, y + 4)  # bottom left of the rock


def tetris(map, n_blocks=2022, check_patterns=False):
    # print(".. starting:", n_blocks)
    jetindex = 0
    extra_by_skipping = 0
    if check_patterns:
        seenheights = []
        seenrocks = []
        seenjets = []
    # for rocknum in range(n_blocks):
    rocknum = -1
    while rocknum < n_blocks - 1:
        rocknum += 1
        # if rocknum % 1000 == 0:
        # print(".... rocks:", rocknum)
        rock = rocks[rocknum % len(rocks)]
        # print("\n".join(rock))
        falling = True
        sx, sy = get_start(map)
        # printmapwithrock(map, rock, (sx,sy))
        while falling:
            # jet (+check collision)
            jeteffect = jet[jetindex]
            if jeteffect == "<":
                newsx = sx - 1
            if jeteffect == ">":
                newsx = sx + 1
            if not check_collision(map, rock, (newsx, sy)):
                sx = newsx
            jetindex = (jetindex + 1) % len(jet)

            # printmapwithrock(map, rock, (sx,sy))

            # fall down (+check collision)
            newsy = sy - 1
            if not check_collision(map, rock, (sx, newsy)):
                sy = newsy
            else:
                falling = False
                putonmap(map, rock, (sx, sy))
                # print("done falling")
                # printmap(map)

        if check_patterns:
            seenheights.append(sy - 4)
            seenjets.append(jetindex)
            seenrocks.append(rocknum % len(rocks))
            # print(seenheights)
            pattern = [str(h2 - h1) for h1, h2 in zip(seenheights, seenheights[1:])]
            # print(pattern)
            for start in range(len(pattern)):
                if start > len(pattern) // 3 or len(pattern) < 50:
                    # no use for short patterns
                    # they'll be doubled as long patterns anyway in future iterations
                    break
                if (len(pattern[start:])) % 2:
                    # odd is annoying, just do the even one
                    continue

                midpoint = (len(pattern[start:]) // 2) + start
                p1 = pattern[start:midpoint]
                p2 = pattern[midpoint:]
                assert len(p1) == len(p2), "lens not same"
                if p1 == p2:
                    # # print(seenheights)
                    # # print(start, ",".join(pattern[start:midpoint]), ",".join(pattern))
                    # print(seenrocks[start], seenrocks[midpoint])
                    assert seenrocks[start] == seenrocks[midpoint]
                    # print(seenjets[start], seenjets[midpoint])
                    assert seenjets[start] == seenjets[midpoint]
                    # print("pattern found after", rocknum, "rocks, lenght", len(p1))
                    # print("patlen:", len(p1))
                    # print("n_blocks:", n_blocks)
                    # print("path times:", (n_blocks-rocknum) // len(p1), ((n_blocks-rocknum) % len(p1)) + rocknum)
                    extra_by_skipping = ((n_blocks - rocknum) // len(p1)) * sum(
                        [int(i) for i in pattern[start:midpoint]]
                    )
                    # print("extra:", extra_by_skipping)
                    # #           blocks to do       blocks to do after path ran
                    #                  v                v
                    new_n_blocks = (
                        (n_blocks - rocknum) % len(p1)
                    ) + rocknum  # < blocks already done
                    # if rocknum >= new_n_blocks-1:
                    #     new_n_blocks += len(p1)
                    # print(
                    #     "n_blocks:", n_blocks,
                    #     ", new n_blocks:", new_n_blocks,
                    #     "diff:", n_blocks-new_n_blocks,
                    #     "cycles:", ((n_blocks-rocknum) // len(p1)),
                    #     " == ", (n_blocks-new_n_blocks)// len(p1)
                    # )
                    n_blocks = new_n_blocks
                    check_patterns = False
    # print()
    # print("simulated", rocknum+1, "rocks")
    return extra_by_skipping


# printmap(map)
# print(len(map))
emptyline = [" " for i in range(7)]
mapp1 = copy.deepcopy(map)
tetris(mapp1)
print("p1:", get_start(mapp1)[1] - 4)
# printmap(mapp1, 20)
# print()

# mapp1pat01 = copy.deepcopy(map)
# extra = tetris(mapp1pat01, 2023, check_patterns=True)
# print("p1 2023:", get_start(mapp1pat01)[1]-4 + extra)
# # printmap(mapp1pat01, 20)
# print()

mapp1pat02 = copy.deepcopy(map)
extra = tetris(mapp1pat02, 2022, check_patterns=True)
print("p1 with pattern:", get_start(mapp1pat02)[1] - 4 + extra)
# printmap(mapp1pat02, 20)
# print()

# mapp1pat03 = copy.deepcopy(map)
# extra = tetris(mapp1pat03, 2021, check_patterns=True)
# print("p1 2021:", get_start(mapp1pat03)[1]-4 + extra)
# # printmap(mapp1pat03, 20)
# print()

# mapp201 = copy.deepcopy(map)
# extra2 = tetris(mapp201, 1000000000000+1, check_patterns = True)
# print("p2 1B+1:", get_start(mapp201)[1]-4 + extra2)
# # printmap(mapp201,20)
# print()

mapp202 = copy.deepcopy(map)
extra2 = tetris(mapp202, 1000000000000, check_patterns=True)
print("p2 1B  :", get_start(mapp202)[1] - 4 + extra2)
# printmap(mapp202,20)
# print()

# mapp203 = copy.deepcopy(map)
# extra2 = tetris(mapp203, 1000000000000-1, check_patterns = True)
# print("p2 1B-1:", get_start(mapp203)[1]-4 + extra2)
# # printmap(mapp203,20)
# print()

# my
#  | 1B-1  |  | 1B    |  | 1B+1  |    | 2021  |  | 2022  |  | 2023  |  | 2024  |
#  |       |  |       |  |       |    |       |  |       |  |       |  |       |
#  |       |  |       |  |       |    |       |  |       |  |       |  |       |
#  |       |  |       |  |       |    |       |  |       |  |       |  |       |
#  |       |  |       |  |       |    |@@@@   |  | @     |  |       |  |       |
#  |       |  |       |  |  @@@@ |    |##     |  |@@@    |  |       |  |       |
#  |       |  |  @@   |  |  ##   |    |##     |  | @     |  |       |  |       |
#  |       |  |  @@   |  |  ##   |    | #     |  |####   |  | #  @  |  |       |
#  |  #  # |  |  #  # |  |  #  # |    | #     |  |##     |  |### @  |  | #  #  |
#  |  #  # |  |  #  # |  |  #  # |    | #  #  |  |##     |  | #@@@  |  |### #  |
#  |  #### |  |  #### |  |  #### |    | #  #  |  | #     |  |####   |  | ####  |
#  |  ##   |  |  ##   |  |  ##   |    | ####  |  | #     |  |##     |  |####   |
#  |  ###  |  |  ###  |  |  ###  |    |#######|  | #  #  |  |##     |  |##     |
#  |   #   |  |   #   |  |   #   |    | ###   |  | #  #  |  | #     |  |##     |
#  |  #### |  |  #### |  |  #### |    |  ##   |  | ####  |  | #     |  | #     |
#  |  ## # |  |  ## # |  |  ## # |    |   #   |  |#######|  | #  #  |  | #    @|
#  |  ## # |  |  ## # |  |  ## # |    |   #   |  | ###   |  | #  #  |  | #  # @|
#  |  #### |  |  #### |  |  #### |    |   ##  |  |  ##   |  | ####  |  | #  # @|
#  | ###   |  | ###   |  | ###   |    |   ##  |  |   #   |  |#######|  | #### @|
#  |  #    |  |  #    |  |  #    |    |  #### |  |   #   |  | ###   |  |#######|

# ---
# test
#  | 1B -1 |  |  1B   |  |  1B+1 |    | 2021  |  | 2022  |  | 2023  |
#  |       |  |       |  |       |    |       |  |       |  |       |
#  |       |  |       |  |       |    |       |  |       |  |       |
#  |       |  |       |  |       |    |       |  |       |  |       |
#  |       |  |       |  |       |    |       |  |   @   |  |       |
#  |       |  |       |  |       |    |       |  |  @@@  |  |  @    |
#  |       |  |       |  |       |    |  @@@@ |  |   @   |  |  @    |
#  |       |  |       |  |  @@@@ |    | ##    |  |  #### |  |@@@#   |
#  |    #  |  |  @@#  |  |  ###  |    | ##   #|  | ##    |  |  ###  |
#  |    #  |  |  @@#  |  |  ###  |    |  #   #|  | ##   #|  |   #   |
#  |  #### |  |  #### |  |  #### |    |  # ###|  |  #   #|  |  #### |
#  |    ###|  |    ###|  |    ###|    |  #  # |  |  # ###|  | ##    |
#  |     # |  |     # |  |     # |    |  # ###|  |  #  # |  | ##   #|
#  | ##### |  | ##### |  | ##### |    | ##### |  |  # ###|  |  #   #|
#  | #  #  |  | #  #  |  | #  #  |    |    #  |  | ##### |  |  # ###|
#  | #  #  |  | #  #  |  | #  #  |    |    #  |  |    #  |  |  #  # |
#  | #### #|  | #### #|  | #### #|    |    #  |  |    #  |  |  # ###|
#  | #### #|  | #### #|  | #### #|    |    #  |  |    #  |  | ##### |
#  |### ###|  |### ###|  |### ###|    | ## #  |  |    #  |  |    #  |
#  | ##### |  | ##### |  | ##### |    | ## #  |  | ## #  |  |    #  |
