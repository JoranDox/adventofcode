# with open("day07inputtest.txt") as f:
with open("day07input.txt") as f:
    data = list(map(int,f.read().split(",")))

# part 1
besti = -1
m = 10000000000000000
for i in range(max(data)+1):
    s = sum([(abs(i-k)) for k in data])
    if s < m:
        m = s
        besti = i
print(besti, m)

# part 2
besti = -1

m = 10000000000000000
for i in range(max(data)+1):
    # s = sum([sum(range(abs(i-k)+1)) for k in data])
    s = sum([((abs(i-k) * (abs(i-k)+1)//2)) for k in data])
    if s < m:
        m = s
        besti = i
print(besti, m)

# print(data)
mediani = sorted(data)[len(data)//2]
medians = sum([(abs(mediani-k)) for k in data])

print(mediani, medians)
import numpy as np
avgi = np.round(sum(data) / len(data))
avgs = list(map(
    lambda i: sum([((abs(i-k) * (abs(i-k)+1)//2)) for k in data]),
    (avgi-1, avgi, avgi+1, avgi+2)
))

avgi = int(np.round(sum(data) / len(data)))
avgs = sum([((abs(i-k) * (abs(i-k)+1)//2)) for k in data])
print(avgi, avgs)