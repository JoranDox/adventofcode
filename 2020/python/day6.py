import functools

accum = 0
accum2 = 0
with open("day6input.txt") as infile:
    # with open("day6inputex.txt") as infile:
    for group in infile.read().strip().split("\n\n"):
        print(group)
        q = set(group) - set("\n")

        print(len(q))
        accum += len(q)
        lst = list(set(line) for line in group.split("\n"))
        combined_set = functools.reduce(lambda a, b: a & b, lst)
        print(combined_set)
        print(len(combined_set))
        accum2 += len(combined_set)


print(accum, accum2)
