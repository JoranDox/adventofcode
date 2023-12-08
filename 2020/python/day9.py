from collections import deque

# real
infilename = "day9input.txt"
last25 = deque(maxlen=25)

# example
# infilename = "day9inputex.txt"
# last25 = deque(maxlen=5)


last25.append(-1)


def checkdeque(num):
    for i in range(len(last25)):
        numi = last25[i]
        for j in range(i + 1, len(last25)):
            numj = last25[j]
            if numi + numj == num:
                return True, numi, numj
    return False, None, None


def checkcontiguous(num):
    for i in range(len(bignumlist)):
        for j in range(i + 1, len(bignumlist)):
            theslice = bignumlist[i:j]
            # print(theslice)
            if sum(theslice) == num:
                return (
                    True,
                    i,
                    j,
                    max(theslice),
                    min(theslice),
                    max(theslice) + min(theslice),
                )


bignumlist = []
with open(infilename) as infile:
    for line in infile:
        bignumlist.append(int(line))

for num in bignumlist:
    if -1 in last25:
        print("adding", num)
        last25.append(num)
        continue

    good, i, j = checkdeque(num)
    print(good, i, j, num)
    if good:
        last25.append(num)
    else:
        print(last25)
        print(num)
        print(checkcontiguous(num))
        break
