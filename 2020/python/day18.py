infilename = "day18input.txt"
# infilename = "day18inputex.txt"

operators = {
    "+": lambda x, y: x + y,
    "*": lambda x, y: x * y,
}


def myeval(line):
    LHS = None
    RHS = None
    op = lambda x, y: y
    while line:
        char = line[0]
        line = line[1:].lstrip()
        # print(f"{LHS=}")
        # print(char)
        if char in "+*":
            op = operators[char]
        elif char in "1234567890":
            # if LHS is None:
            #     LHS = int(char) # there seem to be no numbers over 10
            # else:
            LHS = op(LHS, int(char))
        elif char == "(":
            RHS, line = myeval(line)
            # if LHS is None:
            #     LHS = RHS
            # else:
            LHS = op(LHS, RHS)
        elif char == ")":
            return LHS, line
        else:
            assert False, "oops"
    return LHS


def myeval(line):
    LHS = None
    RHS = None
    op = lambda x, y: y
    while line:
        char = line[0]
        line = line[1:].lstrip()
        # print(f"{LHS=}")
        # print(char)
        if char in "+*":
            op = operators[char]
        elif char in "1234567890":
            # if LHS is None:
            #     LHS = int(char) # there seem to be no numbers over 10
            # else:
            LHS = op(LHS, int(char))
        elif char == "(":
            RHS, line = myeval(line)
            # if LHS is None:
            #     LHS = RHS
            # else:
            LHS = op(LHS, RHS)
        elif char == ")":
            return LHS, line
        else:
            assert False, "oops"
    return LHS


examples = [
    "1 + (2 * 3) + (4 * (5 + 6))",  # becomes 51
    "2 * 3 + (4 * 5)",  # becomes 26.
    "5 + (8 * 3 + 9 + 3 * 4 * 3)",  # becomes 437.
    "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",  # becomes 12240.
    "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2",  # becomes 13632.
]

for line in examples:
    print(line)
    print(myeval(line.strip()))

accum = 0
with open(infilename) as infile:
    for line in infile:
        # print(line, myeval(line.strip()))
        accum += myeval(line.strip())
print(accum)
# part 2
print("part2")


class stupidint:
    def __init__(self, num):
        self.num = num

    def __add__(self, other):
        return stupidint(self.num * other.num)  # lmao

    def __mul__(self, other):
        return stupidint(self.num + other.num)  # lmao

    def __str__(self):
        return str(self.num)

    def __repr__(self):
        return str(self.num)


def numtosto(char):
    if char in "1234567890":
        return f"stupidint({char})"
    elif char == "*":
        return "+"
    elif char == "+":
        return "*"
    else:
        return char


def runassto(line):
    line = "".join([numtosto(char) for char in line])
    return line


examples2 = [
    "1 + (2 * 3) + (4 * (5 + 6))",  # becomes 51
    "2 * 3 + (4 * 5)",  # becomes 46.
    "5 + (8 * 3 + 9 + 3 * 4 * 3)",  # becomes 1445.
    "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",  # becomes 669060.
    "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2",  # becomes 23340.
]

for line in examples2:
    print(line)
    print(runassto(line))
    print(eval(runassto(line)))


accum = 0
with open(infilename) as infile:
    for line in infile:
        # print(line, myeval(line.strip()))
        accum += eval(runassto(line)).num


print(accum)
