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
    # print(cnew)

    # new day here

    print(c.total())