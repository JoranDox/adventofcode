
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
with open(aoc_dir.joinpath("input/2025/day03inputtest.txt")) as f:
# with open(aoc_dir.joinpath("input/2025/day03input.txt")) as f:
    data = f.read().strip()

accum = 0
for line in data.splitlines():
    besttens = -1
    bestones = -1
    for char, nextchar in zip(line, line[1:]):
        t = int(char)
        o = int(nextchar)
        if t > besttens:
            besttens = t
            bestones = o
        if o > bestones:
            bestones = o

    accum += besttens * 10 + bestones
    print(line, accum)

# part2
accum2 = 0
numturnons = 12
for line in data.splitlines():
    turnons = list(line[:numturnons])
    assert len(turnons) == numturnons
    tozip = []
    for i in range(numturnons):
        tozip.append(line[i:])

    for chars in zip(*tozip):
        for i in range(numturnons):
            if chars[i] > turnons[i]:
                turnons[i:] = chars[i:]
    # make it a number
    number = int("".join(turnons))
    accum2 += number
    print(line, number, accum2)

