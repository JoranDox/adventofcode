import copy

infilename = "day21input.txt"
# infilename = "day21inputex.txt"


lines = []
unknownfoods = set()
unknownallergens = set()
knownfoods = {}

allergenpotentials = {}

with open(infilename) as infile:
    for line in infile.read().strip().split("\n"):
        if "(" in line:
            foods, allergens = line.split("(contains ")
            # print(foods, allergens)
            foods = set(foods.split())
            # print(foods, allergens)
            allergens = set(allergens.strip()[:-1].split(", "))
            # print(foods, allergens)
        # else:
        #     print("no allergens")
        #     foods = set(line.split())
        #     allergens = set()
        print(foods, allergens)
        lines.append((foods, allergens))
        print(lines)
        unknownfoods |= foods
        unknownallergens |= allergens
        for allergen in allergens:
            if allergen not in allergenpotentials:
                allergenpotentials[allergen] = {*foods}
            else:
                allergenpotentials[allergen] &= foods


print(lines)

print(allergenpotentials)
cancontain = set()
for allergen, pots in allergenpotentials.items():
    cancontain |= pots
print(f"{unknownfoods=}")
print(f"{cancontain=}")
wannacount = unknownfoods - cancontain
print(f"{wannacount=}")
counter = 0
for foods, allergens in lines:
    for food in wannacount:
        if food in foods:
            counter += 1

print(f"{counter=}")

# part2

found = {}
for i in range(10):
    newfound = {}
    for allergen, pots in allergenpotentials.items():
        if len(pots) == 1:
            newfound[allergen] = list(pots)[0]
    for foundallergen, name in newfound.items():
        del allergenpotentials[foundallergen]
        for allergen, pots in allergenpotentials.items():
            allergenpotentials[allergen] -= set((name,))
    found.update(newfound)

print(found)

print(",".join(found[f] for f in list(sorted(found))))
