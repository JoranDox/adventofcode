# with open("day01inputtest.txt") as infile:
with open("day01input.txt") as infile:
    data = infile.readlines()
    data = [int(x) for x in data]


# part 1
prevline = None
inc = 0
for line in data:
    l = int(line)
    if prevline and l > prevline:
        inc += 1
    prevline = l
print(inc)



# part 2
sums = [sum(x) for x in zip(data[2:], data[1:-1], data[:-2])]
# print(sums[2:-2])
prevline = None
inc = 0
# for s in sums[2:]
for line in sums:
    if prevline and line > prevline:
        inc += 1
    prevline = line
print(inc)
