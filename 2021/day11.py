# with open("day11inputtest.txt") as f:
with open("day11input.txt") as f:
    data = f.read().strip()

octopi = []
for line in data.splitlines():
    octopi.append([int(d) for d in line])

print("\n".join(["".join([str(s) for s in l]) for l in octopi]))
print("\n")
flashcount = 0
step = 0
p1 = False
p2 = False
while True:
    step += 1

    flashed = set()
    tocheck = set()
    octopi = [[d + 1 for d in line] for line in octopi]

    for i, line in enumerate(octopi):
        for j, val in enumerate(line):
            if val > 9:
                # print("flashed", i, j)
                octopi[i][j] = 0
                flashed |= {
                    (i, j),
                }
                flashcount += 1

                for i2 in (-1, 0, 1):
                    for j2 in (-1, 0, 1):
                        icheck = i + i2
                        jcheck = j + j2
                        if icheck < 0:
                            continue
                        if jcheck < 0:
                            continue
                        try:
                            if (icheck, jcheck) not in flashed:
                                octopi[icheck][jcheck] += 1
                                tocheck |= {
                                    (icheck, jcheck),
                                }
                        except IndexError:
                            continue
            # print("\n".join([''.join([str(s) for s in l]) for l in octopi]))
    while tocheck:
        i, j = tocheck.pop()
        if (octopi[i][j] > 9) and ((i, j) not in flashed):
            octopi[i][j] = 0
            flashed |= {
                (i, j),
            }
            flashcount += 1
            for i2 in (-1, 0, 1):
                for j2 in (-1, 0, 1):
                    icheck = i + i2
                    jcheck = j + j2
                    if icheck < 0:
                        continue
                    if jcheck < 0:
                        continue
                    try:
                        if (icheck, jcheck) not in flashed:
                            octopi[icheck][jcheck] += 1
                            tocheck |= {
                                (icheck, jcheck),
                            }
                    except IndexError:
                        continue
    # print("\n".join([''.join([str(s) for s in l]) for l in octopi]))
    # print(flashed)
    if step == 100:
        print("part 1:")
        print(flashcount)
        p1 = True
    if all([not any(line) for line in octopi]):
        print("part 2")
        print(step)
        p2 = True
    if p1 & p2:
        break
