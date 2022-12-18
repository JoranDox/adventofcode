import ast
import functools
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
#with open(aoc_dir.joinpath("input/2022/day13inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day13input.txt")) as f:
    data = f.read().strip()


packets = [[ast.literal_eval(p_) for p_ in p.splitlines()] for p in data.split("\n\n")]

# print(packets[0])

def compare(left,right):
    # ternary comparison:
    # return -1 if left < right
    # return 0 if left == right
    # return 1 if left > right
    if left == right:
        return 0
    if type(left) == type(right) == int:
        if left < right: # equal is handled above
            return -1
        if left > right:
            return 1
    if type(left) == type(right) == list:
        for l,r in zip(left,right):
            res = compare(l,r)
            if res is not 0:
                return res
        if len(left) < len(right): # equal is handled above
            return -1
        if len(left) > len(right): # equal is handled above
            return 1
        if len(left) == len(right): # this covers cases like [[9]] ? [9], sigh
            return 0
    if (type(left) == int) and (type(right) == list):
        return compare([left], right)
    if (type(left) == list) and (type(right) == int):
        return compare(left, [right])

accum = 0
for i, (p1, p2) in enumerate(packets):
    c = compare(p1,p2)
    # print(i, p1, p2, c)
    if c == -1:
        accum += i + 1
print("p1:", accum)

packets2 = [ast.literal_eval(p) for p in data.splitlines() if p]
packets2.append([[2]])
packets2.append([[6]])
sp2 = sorted(packets2, key=functools.cmp_to_key(compare))
# print("sorted")
# for line in sp2:
#     print(line)
# print()
i1 = sp2.index([[2]])+1
i2 = sp2.index([[6]])+1
print(i1, i2, i1 * i2)