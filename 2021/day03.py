# with open("day03inputtest.txt") as f:
with open("day03input.txt") as f:
    data = f.readlines()

basecount = [0, 0]

counts = []

for line in data:
    for n, char in enumerate(line.strip()):
        c = int(char)
        if n >= len(counts):
            counts.append(basecount.copy())
        counts[n][c] += 1

print(counts)

gamma = ""
epsilon = ""
for i, j in counts:
    if i > j:
        gamma += "0"
        epsilon += "1"
    else:
        gamma += "1"
        epsilon += "0"
print(gamma)
print(epsilon)

print(int(gamma, 2))
print(int(epsilon, 2))

print(int(gamma, 2) * int(epsilon, 2))

print("part2")

# binaries = [int(line,2) for line in data]
# print(binaries)

oxygen = [d.strip() for d in data]
oxy = ""
while True:
    zeroes = len([o for o in oxygen if o.startswith("0")])
    ones = len([o for o in oxygen if o.startswith("1")])

    if zeroes > ones:
        oxy += "0"
        oxygen = [o[1:] for o in oxygen if o.startswith("0")]
    else:
        oxy += "1"
        oxygen = [o[1:] for o in oxygen if o.startswith("1")]
    if len(oxygen) == 1:
        print("found", oxy, oxygen)
        break

co2list = [d.strip() for d in data]
co2 = ""
while True:
    zeroes = len([o for o in co2list if o.startswith("0")])
    ones = len([o for o in co2list if o.startswith("1")])

    if zeroes > ones:
        co2 += "1"
        co2list = [o[1:] for o in co2list if o.startswith("1")]
    else:
        co2 += "0"
        co2list = [o[1:] for o in co2list if o.startswith("0")]
    if len(co2list) == 1:
        print("found", co2, co2list)
        break
print(
    oxy + oxygen[0], co2 + co2list[0], int(oxy + oxygen[0], 2), int(co2 + co2list[0], 2)
)
print(int(oxy + oxygen[0], 2) * int(co2 + co2list[0], 2))
