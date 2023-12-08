infilename = "day10input.txt"
# infilename = "day10inputex.txt"
# infilename = "day10inputexsmall.txt"


bignumlist = []
with open(infilename) as infile:
    for line in infile:
        bignumlist.append(int(line))

bignumlist = sorted(bignumlist)

diffs = [j - i for i, j in zip([0, *bignumlist], [*bignumlist, bignumlist[-1] + 3])]
from collections import Counter

c = Counter(diffs)

print(c)
print(c[1] * c[3])  # answer to part one

# #part2
# waystogetto = [1]
# steps =
# for i in range(0, bignumlist[-1]):

#     if bignumlist[i]


# start at pos 0
# jump 1, 2 or 3
print(bignumlist)

waystogetto = [0] * (bignumlist[-1] + 1)
waystogetto[0] = 1
for i in bignumlist:
    # print(i)
    # print(waystogetto)
    # print(waystogetto[i-3:i])
    # print(waystogetto[max(0,i-3):i])
    # print(i-3, i)
    waystogetto[i] = sum(waystogetto[(0, i - 3) : i])

print(waystogetto)
