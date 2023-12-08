import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day25inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day25input.txt")) as f:
    data = f.read().strip()

snafumap = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}
print(snafumap)
revsnafumap = {((v + 5) % 5): k for k, v in snafumap.items()}
print(revsnafumap)


def snafutranslator(snafunum):
    accum = 0
    for x in snafunum:
        accum *= 5
        accum += snafumap[x]
    return accum


def reversesnafu(normalnum):
    # print(normalnum)
    snafunum = []
    while normalnum:
        remainder = normalnum % 5
        snafunum.append(revsnafumap[remainder])
        if remainder > 2:
            normalnum += 5
        normalnum = normalnum // 5
        # print(snafunum[::-1])
    return "".join(snafunum[::-1])


bigaccum = 0
for line in data.splitlines():
    s = snafutranslator(line)
    print(line.rjust(20), end="", flush=True)
    print(str(s).rjust(15), end="", flush=True)
    print(reversesnafu(s).rjust(20), end="", flush=True)
    assert line == reversesnafu(s)
    print()
    bigaccum += s
print(bigaccum, reversesnafu(bigaccum))
# for line in data.split("\n\n"):
