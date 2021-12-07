# with open("day07inputtest.txt") as f:
with open("day07input.txt") as f:
    data = list(map(int,f.read().split(",")))

# part 1
m = 10000000000000000
for i in range(max(data)+1):
    s = sum([(abs(i-k)) for k in data])
    m = min(m,s)
print(i, s, m)

# part 2
m = 10000000000000000
for i in range(max(data)+1):
    # s = sum([sum(range(abs(i-k)+1)) for k in data])
    s = sum([((abs(i-k) * (abs(i-k)+1)//2)) for k in data])
    m = min(m,s)
print(i, s, m)

# print(data)