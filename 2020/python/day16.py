# class: 1-3 or 5-7
# row: 6-11 or 33-44
# seat: 13-40 or 45-50

# your ticket:
# 7,1,14

# nearby tickets:
# 7,3,47
# 40,4,50
# 55,2,20
# 38,6,12


filename = "day16input.txt"
# filename = "day16inputex.txt"
# filename = "day16inputex2.txt"


minnum = 1000
maxnum = 0


def maprules(inrules):
    global minnum
    global maxnum
    lst = inrules.split("\n")

    ret = {}
    for rule in lst:
        temp = []
        name, rest = rule.split(": ")
        restsplit = rest.split(" or ")
        for subrule in restsplit:
            low, high = subrule.split("-")
            low, high = int(low), int(high)
            minnum = min(minnum, low)
            maxnum = max(maxnum, high)
            temp.append((low, high))
        ret[name] = temp
    return ret


def maptickets(intickets):
    lst = intickets.split("\n")
    print(lst[0])
    return [tuple(map(int, ticket.split(","))) for ticket in lst[1:]]


with open(filename) as infile:
    rules, yourticket, neartickets = infile.read().strip().split("\n\n")
    rules = maprules(rules)
    yourticket = maptickets(yourticket)[0]
    neartickets = maptickets(neartickets)

print(minnum, maxnum)

print(rules, yourticket, neartickets)

validnums = set()

for rule in rules.values():
    for low, high in rule:
        validnums |= set(range(low, high + 1))
        # print(validnums)


accum = 0
validtickets = [yourticket]
for ticket in neartickets:
    isvalid = True
    for num in ticket:
        if num not in validnums:
            isvalid = False
            # print(num)
            accum += num
    if isvalid:
        validtickets.append(ticket)

print(accum)

import pandas as pd

df = pd.DataFrame(validtickets)
print(df)

validnums = set()
rules2 = {}
for name, rule in rules.items():
    ruleset = set()
    for low, high in rule:
        ruleset |= set(range(low, high + 1))
    rules2[name] = ruleset
print(rules2)

unusednames = set(rules2.keys())
unusedcolumns = set(range(len(yourticket)))

while unusednames:
    for col in unusedcolumns:
        print(col)
        # print(df[col])
        validnames = []
        for rulename, ruleset in rules2.items():
            print("  ", rulename)
            if df[col].isin(ruleset).all():
                validnames.append(rulename)
        assert len(validnames) != 0, "shit"
        if len(validnames) == 1:
            break  # avoid RuntimeError: Set changed size during iteration
    if len(validnames) == 1:
        rightrule = validnames[0]
        rightcol = col
        print("correct1:", rightcol, rightrule)
        df = df.rename(columns={rightcol: rightrule})
        unusednames -= set((rightrule,))
        unusedcolumns -= set((rightcol,))
        del rules2[rightrule]
        continue

    for rulename, ruleset in rules2.items():
        print(rulename)
        validnames = []
        for col in unusedcolumns:
            print("  ", col)
            # print(df[col])
            if df[col].isin(ruleset).all():
                validnames.append(col)
        assert len(validnames) != 0, "shit"
        if len(validnames) == 1:
            break
    if len(validnames) == 1:
        rightrule = rulename
        rightcol = validnames[0]
        print("correct2:", rightcol, rightrule)
        df = df.rename(columns={rightcol: rightrule})
        unusednames -= set((rightrule,))
        unusedcolumns -= set((rightcol,))
        del rules2[rightrule]
        continue
print(unusednames)
print(df)
accum = 1
for col in df:
    if col.startswith("departure"):
        accum *= df[col][0]
        print(df[col][0])
print(accum)
