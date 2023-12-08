infilename = "day19inputex.txt"
infilename = "day19inputex2.txt"
infilename = "day19input.txt"


with open(infilename) as infile:
    rules, messages = infile.read().strip().split("\n\n")
print(rules)

parsedrules = {}
for rule in rules.split("\n"):
    parsedrule = []
    spl = rule.split(":")

    index = int(spl[0])
    ### start part 2
    if index == 8:
        spl = (8, "42 | 42 8")
    if index == 11:
        spl = (11, "42 31 | 42 11 31")
    ### end part 2
    for r in spl[1].strip().split(" "):
        r = r.strip('"')
        try:
            r = int(r)
        except:
            pass
        parsedrule.append(r)

    parsedrules[index] = parsedrule

print(parsedrules)


messages = messages.split("\n")

dprint = lambda *x, **y: None
import sys

sys.setrecursionlimit(10000)


def rule0(message):
    count42 = 0
    count31 = 0
    while True:
        r, message = validate(message, parsedrules[42])
        if r:
            count42 += 1
            m2 = message
            for i in range(count42):
                r2, m2 = validate(
                    m2, parsedrules[11]
                )  # this is a typo but gives the right answer ???
                if not r2:
                    break
                if r2 and not m2:
                    return True
        else:
            return False


def validate(message, rule):
    # rule is one of:
    # [2, 3, '|', 3, 2]
    # ['a']
    # [4, 1, 5]
    dprint("in:", message, rule)
    if len(rule) == 0:
        # trivial case
        dprint("empty rule")
        return True, message
    elif len(message) == 0:
        dprint("empty message")
        return False, message
    elif "|" in rule:
        dprint("'or' rule")
        i = rule.index("|")
        r, m = validate(message, rule[:i])
        if r:
            return r, m
        else:
            return validate(message, rule[i + 1 :])
    elif len(rule) > 1 and type(rule[0]) == int:
        dprint("'and' rule")
        r, m = validate(message, parsedrules[rule[0]])
        if r:
            return validate(m, rule[1:])
        else:
            return r, m
    elif len(rule) == 1 and type(rule[0]) == int:
        dprint("deref rule")
        return validate(message, parsedrules[rule[0]])
    elif len(rule) == 1 and type(rule[0]) == str:
        dprint("match rule")
        if message[0] == rule[0]:
            return True, message[1:]
        else:
            return False, message[1:]
    assert False, "shouldn't have come here"


def validate2(message, rule):
    # rule is one of:
    # [2, 3, '|', 3, 2]
    # ['a']
    # [4, 1, 5]
    dprint("in:", message, rule)
    if len(rule) == 0:
        # trivial case
        dprint("empty rule")
        return True, message
    elif len(message) == 0:
        dprint("empty message")
        return False, message
    elif "|" in rule:
        dprint("'or' rule")
        i = rule.index("|")
        r, m = validate(message, rule[:i])
        if r:
            return r, m
        else:
            return validate(message, rule[i + 1 :])
    elif len(rule) > 1 and type(rule[0]) == int:
        dprint("'and' rule")
        for char in rule:
            r, m = validate(message, char)
        if r:
            return validate(m, rule[1:])
        else:
            return r, m
    elif len(rule) == 1 and type(rule[0]) == int:
        dprint("deref rule")
        return validate(message, parsedrules[rule[0]])
    elif len(rule) == 1 and type(rule[0]) == str:
        dprint("match rule")
        if message[0] == rule[0]:
            return True, message[1:]
        else:
            return False, message[1:]
    assert False, "shouldn't have come here"


accum = 0
for message in messages:
    print("toplevel:", message)
    r, m = validate(message, parsedrules[0])
    r &= len(m) == 0
    if r:
        accum += 1
print(accum)

print("part2")
accum = 0
for message in messages:
    print("toplevelpart2:", message)
    if rule0(message):
        accum += 1
print(accum)
