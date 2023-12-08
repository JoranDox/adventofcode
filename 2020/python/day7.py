bags = dict()
bagspart2 = dict()
filename = "joeriinput.txt"
filename = "day7input.txt"

with open(filename) as infile:
    for line in infile:
        outerbagtype, innerbags = line.strip()[:-1].split(" contain ", 1)
        outerbagtype = " ".join(outerbagtype.split()[:-1])  # remove "bag(s)"
        for bag in innerbags.split(", "):
            num, innerbagtype = bag.split(" ", 1)
            innerbagtype = " ".join(innerbagtype.split()[:-1])  # remove "bag(s)"
            if innerbagtype not in bags:
                bags[innerbagtype] = []
            if outerbagtype not in bagspart2:
                bagspart2[outerbagtype] = []
            bags[innerbagtype].append(outerbagtype)
            if num == "no":
                continue
            bagspart2[outerbagtype].append((innerbagtype, int(num)))

to_search = ["shiny gold"]
seen = []

while to_search:
    bag = to_search.pop()
    if bag in seen:
        continue
    seen.append(bag)
    for newbag in bags.get(bag, []):
        to_search.append(newbag)

# print(seen)

print(len(seen) - 1)


to_search = [("shiny gold", 1)]
seen = []
counter = 0
while to_search:
    bag, num = to_search.pop()
    # print(bag, num)
    counter += num
    for newbag, newbagnum in bagspart2.get(bag, []):
        to_search.append((newbag, newbagnum * num))

# print(seen)
print(counter - 1)
