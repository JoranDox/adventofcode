filename = "day15input.txt"
# filename = "day15inputex.txt"
with open(filename)as infile:
    startingnumbers = list(map(int, infile.read().strip().split(",")))
print(startingnumbers)


# from collections import deque

# d = deque(reversed(startingnumbers))

# for i in range(len(d), 2020):
#     lastnum = d[0]
#     try:
#         age = d.index(lastnum, 1)
#     except ValueError:
#         age = 0
#     # print(age)
#     d.appendleft(age)

# print(list(reversed(d)))
# # print([i-j for i,j in zip([0, *d], [*d, 0])])
# print(max(d))


# writing it with a dict instead

lastsaid = {n:i for i,n in enumerate(startingnumbers[:-1])}

prev = startingnumbers[-1]
for i in range(len(startingnumbers), 30000000):
    if not i % 100000:
        print(i)
    last = lastsaid.get(prev, None)
    if last is not None:
        age = i - last - 1
    else:
        age = 0
    lastsaid[prev] = i-1
    prev = age

print(prev)
# modnum = 1
# for i in range(len(d), 30000000):
#     if not i % modnum:
#         print(i)
#         modnum *= 2
#     lastnum = d[0]
#     try:
#         age = d.index(lastnum, 1)
#     except ValueError:
#         age = 0
#     d.appendleft(age)

# print(age)
