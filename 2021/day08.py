# with open("day08inputtest.txt") as f:
with open("day08input.txt") as f:
    data = f.readlines()

# constants
#       0  1  2  3  4  5  6  7  8  9
lens = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]
maps = [
    s.replace(" ", "")
    for s in [
        "abc efg",  # 0
        "  c  f ",  # 1
        "a cde g",  # 2
        "a cd fg",  # 3
        " bcd f ",  # 4
        "ab d fg",  # 5
        "ab defg",  # 6
        "a c  f ",  # 7
        "abcdefg",  # 8
        "abcd fg",  # 9
    ]
]


subsets = [
    [set(maps[n]).issubset(set(maps[n2])) for n2 in range(10)] for n in range(10)
]
print(f"{subsets}")

intersections = [
    [set(maps[n]) & (set(maps[n2])) for n2 in range(10)] for n in range(10)
]
print(f"{intersections=}")


def letters_to_num(letters, known_maps):
    return known_maps.index(letters)


print(set("abcdefg"))

# part1
count = 0
for d in data:
    print(d.strip())
    ind, outd = d.split("|")
    indsplit = ["".join(sorted(d2)) for d2 in ind.strip().split()]
    outdsplit = ["".join(sorted(d2)) for d2 in outd.strip().split()]
    count += len([d2 for d2 in outdsplit if len(d2) in (2, 3, 4, 7)])
    # print(sorted(set(indsplit)))
    # print(sorted(set(outdsplit)))

    # part2
    known_maps = ["" for i in range(10)]
    potential_maps = [set("abcdefg") for i in range(10)]
    mapping = {l: set("abcdefg") for l in "abcdefg"}
    # print(mapping)
    iters = 0
    progress = 0
    continue  # skip the below code
    while not all([outdsplit in known_maps]):
        iters += 1
        progress -= 1
        # print(iters, lens)
        for n, l in enumerate(lens):
            # print(f"{n=},{l=}")
            # print(f"{known_maps=}")
            # print(f"{potential_maps=}")
            # print(f"{mapping=}")

            # n is the number we're checking
            # l is the expected length
            if len(known_maps[n]) > 0:
                # print('skipping', n, known_maps[n])
                continue
            candidates = {i for i in [*indsplit, *outdsplit] if len(i) == l}
            # todo: eliminate candidates based on existing mapping
            # print(f"{candidates=}")
            superset = set()
            for c in candidates:
                superset |= set(c)
            # print(f"{superset=}")
            potential_maps[n] &= superset
            for letter in maps[n]:
                mapping[letter] &= superset

            # print(f"{potential_maps=}")
            # filter using potential_maps
            candidates = {
                c for c in candidates if all([_c in potential_maps[n] for _c in c])
            }
            # print(f"{candidates=}")

            # print(f"{mapping=}")

            # filter using mapping (? how ?)
            candidates = {c for c in candidates}

            # print(f"{candidates=}")
            if len(candidates) > 1:
                # print('skipping too many candidates')
                continue
            # we now have a candidate for a number based on length
            progress += 1
            # print(progress)
            c = list(candidates)[0]
            print("found", n, c)
            known_maps[n] = c
            for letter in maps[n]:
                mapping[letter] &= set(c)
        print(progress)

        # map_intersects
        if progress < 0 or iters > 100:
            print("no progress")
            break

    # try to brute force the rest here
    print(d)
    print(f"{known_maps=}")
    print(f"{potential_maps=}")
    print(f"{mapping=}")

    # print('yay', [letters_to_num(ls) for ls in outdsplit])
    break

    print(d.strip())

# part1
print(count)

# part 2 with frequencies
from collections import Counter

c = Counter()
for m in maps:
    c.update(m)
print(c)


def replace(instr, mapping):
    return "".join(sorted([mapping[c] for c in instr]))


total = 0
for d in data:
    # print(d.strip())
    ind, outd = d.split("|")
    indsplit = ["".join(sorted(d2)) for d2 in ind.strip().split()]
    outdsplit = ["".join(sorted(d2)) for d2 in outd.strip().split()]
    bothd = [*indsplit, *outdsplit]
    unique = set(bothd)
    assert len(unique) == 10
    c2 = Counter()
    for m in unique:
        c2.update(m)
    # print(c2, list(c2.keys()))
    mapping_rev = {
        a: b
        for a, b in zip(
            [i_[0] for i_ in c.most_common()], [i_[0] for i_ in c2.most_common()]
        )
    }

    # 4 possible mappings
    mappings = []
    mappings.append({v: k for k, v in mapping_rev.items()})
    mapping_rev["a"], mapping_rev["c"] = mapping_rev["c"], mapping_rev["a"]
    mappings.append({v: k for k, v in mapping_rev.items()})
    mapping_rev["g"], mapping_rev["d"] = mapping_rev["d"], mapping_rev["g"]
    mappings.append({v: k for k, v in mapping_rev.items()})
    mapping_rev["a"], mapping_rev["c"] = mapping_rev["c"], mapping_rev["a"]
    mappings.append({v: k for k, v in mapping_rev.items()})
    for m in mappings:
        print(m)
    possibles = set()
    for mapping in mappings:
        # print(mapping)
        outdsplit2 = [replace(d2, mapping) for d2 in outdsplit]
        # print(outdsplit)
        # print(outdsplit2)
        try:
            output = [maps.index(d2) for d2 in outdsplit2]
            # print(output)
            n = 0
            for i in output:
                n *= 10
                n += i
            possibles |= {
                n,
            }

            total += n
            break
        except ValueError:
            pass
    # assert good == 1, good
    if len(possibles) != 1:
        print(possibles)
    assert len(possibles) == 1
    # break

print(total)
