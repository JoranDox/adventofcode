from collections import Counter, defaultdict

# with open("day14inputtest.txt") as f:
with open("day14input.txt") as f:
    data = f.read().strip()

input, others = data.split("\n\n")
firstinput = input
print(input)
print(others)
insertions = dict(line.split(" -> ") for line in others.splitlines())

print(insertions)


def insert(text):
    prev = text[0]
    new = []
    new.append(prev)
    for i in text[1:]:
        if (prev + i) in insertions:
            new.append(insertions[prev + i])
        new.append(i)
        prev = i
    return new


for i in range(10):
    input = insert(input)
print("".join(input))
print(Counter("".join((i, j)) for i, j in zip(input, input[1:])))
c = Counter(input)
mc = c.most_common()
print(c)
print(mc[0][1], mc[-1][1])
print("part1:")
print(mc[0][1] - mc[-1][1])


print("part2:")

inputsplit = Counter("".join((i, j)) for i, j in zip(firstinput, firstinput[1:]))
print(firstinput, inputsplit)


def insert2(incounter):
    newcounter = defaultdict(lambda: 0)
    for bigram, count in incounter.items():
        # print(bigram, count)
        if bigram in insertions:
            i = insertions[bigram]
            bigram[0] + i
            newcounter[bigram[0] + i] += count
            newcounter[i + bigram[1]] += count
        else:
            newcounter[bigram] += count
    return newcounter


first = firstinput[0]
last = firstinput[-1]


def countdoubles(incounter):
    midcounter = Counter()
    for bigram, count in incounter.items():
        midcounter.update({bigram[0]: count})
        midcounter.update({bigram[1]: count})
    midcounter.update({first: 1})
    midcounter.update({last: 1})

    outcounter = {i: j // 2 for i, j in midcounter.items()}

    return outcounter


insert2(inputsplit)
for i in range(40):
    inputsplit = insert2(inputsplit)
print(inputsplit)
c = Counter(countdoubles(inputsplit))
mc = c.most_common()
print(c)
print(mc[0][1], mc[-1][1])

print("part2:")
print(mc[0][1] - mc[-1][1])
