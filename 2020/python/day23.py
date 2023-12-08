example = "389125467"
real = "186524973"
inputcups = example
inputcups = real

cups = tuple(int(i) for i in inputcups)
m = max(cups)


def oneround(cups):
    cup = cups[0]
    liftedcups = cups[1:4]
    othercups = cups[4:]

    searchcup = cup

    while searchcup not in othercups:
        searchcup = searchcup - 1
        if searchcup == 0:
            searchcup = m
    ind = othercups.index(searchcup) + 1

    return (*othercups[:ind], *liftedcups, *othercups[ind:], cup)


# part1
for i in range(100):
    cups = oneround(cups)
    print(cups)
print(cups)

# part 2
print("part2")
from dataclasses import dataclass


@dataclass
class num:
    v: int
    n: object = None


# cups = (*tuple(int(i) for i in inputcups), )
cups = (*tuple(int(i) for i in inputcups), *range(m + 1, 1000001))
m = max(cups)

cups = tuple(num(v=i) for i in cups)
for cup, nex in zip(cups, cups[1:]):
    cup.n = nex
cups[-1].n = cups[0]

links = {c.v: c for c in cups}

it = links[int(inputcups[0])]

icomp = 10

# for i in range(100):
for i in range(9999999):
    if not i % icomp:
        print(i)
        icomp *= 10
    cup1 = it
    cup2 = cup1.n
    cup3 = cup2.n
    cup4 = cup3.n
    cupinsertn = cup1.v - 1
    comps = (cup2.v, cup3.v, cup4.v, 0)
    while cupinsertn in comps:
        if not cupinsertn:
            cupinsertn = m
        else:
            cupinsertn -= 1
    # triple swap
    links[cupinsertn].n, cup1.n, cup4.n = cup2, cup4.n, links[cupinsertn].n
    it = cup1.n

cup1 = it
cup2 = cup1.n
cup3 = cup2.n
cup4 = cup3.n
cupinsertn = cup1.v - 1
comps = (cup2.v, cup3.v, cup4.v, 0)
while cupinsertn in comps:
    if not cupinsertn:
        cupinsertn = m
    else:
        cupinsertn -= 1
# triple swap
links[cupinsertn].n, cup1.n, cup4.n = cup2, cup4.n, links[cupinsertn].n
it = cup1.n
print(m)
c = links[1]
for i in range(10):
    print(c.v, end=" ")
    c = c.n
print()

cup1 = it
cup2 = cup1.n
cup3 = cup2.n
cup4 = cup3.n
cupinsertn = cup1.v - 1
comps = (cup2.v, cup3.v, cup4.v, 0)
while cupinsertn in comps:
    if not cupinsertn:
        cupinsertn = m
    else:
        cupinsertn -= 1
# triple swap
links[cupinsertn].n, cup1.n, cup4.n = cup2, cup4.n, links[cupinsertn].n
it = cup1.n

c = links[1]
for i in range(10):
    print(c.v, end=" ")
    c = c.n
print()
cup1 = it
cup2 = cup1.n
cup3 = cup2.n
cup4 = cup3.n
cupinsertn = cup1.v - 1
comps = (cup2.v, cup3.v, cup4.v, 0)
while cupinsertn in comps:
    if not cupinsertn:
        cupinsertn = m
    else:
        cupinsertn -= 1
# triple swap
links[cupinsertn].n, cup1.n, cup4.n = cup2, cup4.n, links[cupinsertn].n
it = cup1.n

c = links[1]
for i in range(10):
    print(c.v, end=" ")
    c = c.n
print()
# seen = set((cups,))
# icomp = 10
# for i in range(10000000):
#     if not i % icomp:
#         print(i)
#         icomp *= 10
#     cups = oneround(cups)
#     if set((cups,)) in seen:
#         print(i)
#         break
# ind = cups.index(1)
# print(cups[ind+1], cups[ind+2], cups[ind+1] * cups[ind+2])
