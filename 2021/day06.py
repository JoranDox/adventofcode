from collections import Counter
# with open("day06inputtest.txt") as f:
with open("day06input.txt") as f:
    data = f.read()

data = [int(d) for d in data.split(",")]

c = Counter(data)
print(data)
print(c)
print(c[3])
nbabies = c[0]
cnew = c

# for day in range(81):
for day in range(257):

    cnew.update({
        6: nbabies,
        8: nbabies
    })
    c = cnew

    nbabies = c[0]
    cnew = Counter(
        {
            i-1: k for i,k in c.items() if i and k
        }
    )

print(c.total())

# naive way, works for 80 but takes insanely long for 256:

data2 = [d for d in data]
for day in range(80):
# import tqdm
# for day in tqdm.tqdm(range(256)): # this takes too long
# 65%|██████▌   | 167/256 [13:44<1:26:16, 58.17s/it]
    datanew = []
    for d in data2:
        if d == 0:
            datanew.append(6)
            datanew.append(8)
        else:
            datanew.append(d-1)
    data2 = datanew
    print(len(data2))