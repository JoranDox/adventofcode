import numpy as np
import collections

# with open("day05inputtest.txt") as f:
with open("day05input.txt") as f:
    data = f.readlines()

data = [ d.split("->") for d in data ]
data = [(*i.split(","), *j.split(",")) for i,j in data]
data = [[int(i) for i in d] for d in data]
data = [((i,j),(k,l)) for i,j,k,l in data]

# print(data)

datahor = [
    ((i,j),(k,l)) for ((i,j),(k,l)) in data
    if i == k
]
# print(datahor)
dataver = [
    ((i,j),(k,l)) for ((i,j),(k,l)) in data
    if j == l
]
# print(dataver)
def makehorline(startend):
    (i,j),(k,l) = startend
    
    return (
        { (i,i2) for i2 in range(j,l+1)} |
        { (i,i2) for i2 in range(l,j+1)}
    )


def makeverline(startend):
    (i,j),(k,l) = startend

    return (
        { (i2,j) for i2 in range(i,k+1)} |
        { (i2,j) for i2 in range(k,i+1)}
    )

# print(datahor[1])
# print(makehorline(datahor[1]))

s = list()
for d in datahor:
    s.extend(makehorline(d))
for d in dataver:
    s.extend(makeverline(d))
# print(s)
# print([*[makehorline(d) for d in datahor], *[makeverline(d) for d in dataver]])
c = collections.Counter(s)
# print(c)
print(len([_ for l,p in c.most_common() if p >= 2]))

def makeline(startend):
    (i,j),(k,l) = startend

    # assert (i==k) or (j==l) or abs(l-j) == abs(k-i)
    
    hdir = (l-j)//abs(l-j)
    vdir = (k-i)//abs(k-i)
    r1 = range(0, abs(l-j)+1)
    # print(r1)
    

    # l = list()
    s = set()
    for i2 in r1:
        # l.append((i+i2*vdir, j+i2*hdir))
        s |= {(i+i2*vdir, j+i2*hdir)}
    # print(l)
    return s

datadiag = [d for d in data if d not in dataver and d not in datahor]
# print(datadiag)
# s = list()
for d in datadiag:
    s.extend(makeline(d))

c = collections.Counter(s)

# print(c)
print(len([_ for l,p in c.most_common() if p >= 2]))
