import math
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2025/day06inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2025/day06input.txt")) as f:
    data = f.read().strip()

grandtotal = 0
lines = data.splitlines()
lines = [
    [int(part) if part not in "*+" else part for part in line.split()] for line in lines
]
for *vars, op in zip(*lines):
    match op:
        case "+":
            result = sum(vars)
        case "*":
            result = math.prod(vars)
        case _:
            assert False, f"Unknown operator: {op}"
    grandtotal += result
print(grandtotal)

# part 2
lines = [l + "   " for l in data.splitlines()] # add padding
op = None
grandtotal2 = 0
tempresult = 0
for *chars, operator in zip(*lines):
    print(chars, operator)
    match operator:
        case "+":
            grandtotal2 += tempresult
            print(grandtotal2, tempresult)
            tempresult = 0
            op = sum
        case "*":
            grandtotal2 += tempresult
            print(grandtotal2, tempresult)
            tempresult = 1
            op = math.prod
        case " ":
            pass
        case _:
            assert False, f"Unknown operator: {operator}"
    assert op is not None
    print(chars)
    snum = "".join(chars)
    print(snum)
    try:
        num = int(snum)
        tempresult = op((tempresult, num))
        print("t", tempresult)
    except ValueError:
        print(f"Invalid number: {snum}")

grandtotal2 += tempresult
print(grandtotal2)