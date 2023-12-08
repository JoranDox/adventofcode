# with open("day15inputtest.txt") as f:
with open("day15input.txt") as f:
    data = f.read().strip()

alot = 10000
mymap = [[(int(d), alot) for d in line] for line in data.splitlines()]


def doapass(mymap):
    for i, line in enumerate(mymap):
        for j, (val, risk) in enumerate(line):
            if i == j == 0:
                mymap[i][j] = (val, 0)
                continue
            up = left = down = right = alot
            if i > 0:
                up = mymap[i - 1][j][1]
            if j > 0:
                left = mymap[i][j - 1][1]
            if i < len(mymap) - 1:
                down = mymap[i + 1][j][1]
            if j < len(mymap[0]) - 1:
                right = mymap[i][j + 1][1]

            mymap[i][j] = (val, val + min(up, left, down, right))


result = 0
while True:
    doapass(mymap)
    newresult = mymap[-1][-1][1]
    if newresult != result:
        print("intermediary result:", newresult)
        result = newresult
    else:
        print("done", result)
        break

import numpy as np

mymap = np.array([[int(d) for d in line] for line in data.splitlines()])

# print(mymap)
# print((mymap + 1) % 10)
# print(mymap)

mybigmap1 = np.concatenate([((mymap + x - 1) % 9) + 1 for x in range(5)])

mybigmap2 = np.concatenate([((mybigmap1 + x - 1) % 9) + 1 for x in range(5)], axis=1)
# [print(line) for line in mybigmap2]
# print(mybigmap2.shape)

mybigrisks2 = np.zeros(mybigmap2.shape) + alot
mybigrisks2[0][0] = 0
# [print(line) for line in mybigrisks2]
# print(mybigrisks2.shape)


def doapass2(mymap, risks):
    for i, line in enumerate(mymap):
        for j, val in enumerate(line):
            if i == j == 0:
                risks[i][j] = 0
                continue
            up = left = down = right = alot
            if i > 0:
                up = risks[i - 1][j]
            if j > 0:
                left = risks[i][j - 1]
            if i < len(mymap) - 1:
                down = risks[i + 1][j]
            if j < len(mymap[0]) - 1:
                right = risks[i][j + 1]

            risks[i][j] = val + min(up, left, down, right)


prevrisks = mybigrisks2.copy()
steps = 0
while True:
    steps += 1
    doapass2(mybigmap2, mybigrisks2)
    result = mybigrisks2[-1][-1]
    if (prevrisks - mybigrisks2).any():
        print(f"intermediary result after {steps} steps: {result}")
        prevrisks = mybigrisks2.copy()
    else:
        print("done", result)
        break
        # not sure what the right exit condition is
        # break
