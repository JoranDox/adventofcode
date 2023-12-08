import functools
import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day11inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day11input.txt")) as f:
    data = f.read().strip()

# for line in data.splitlines():

monkeys = []
for monkey in data.split("\n\n"):
    monkeyname, starting, operation, test, true, false = monkey.splitlines()
    n0, eq, n1, op, n2 = operation.split(": ")[1].split()
    assert n0 == "new"
    assert eq == "="

    assert test.startswith("  Test: divisible by")
    monkeys.append(
        {
            "items": [int(x) for x in starting.split(": ")[1].split(", ")],
            "operation": (op, n1, n2),
            "test": int(test.split(" ")[-1]),
            True: int(true.split(" ")[-1]),
            False: int(false.split(" ")[-1]),
            "counter": 0,
        }
    )

print([m["test"] for m in monkeys])

divisor = functools.reduce(lambda x, y: x * y, [m["test"] for m in monkeys])
print(divisor)
print(monkeys)
for mround in range(10000):
    for monkey in monkeys:
        # print(monkey)
        for worryval in monkey["items"]:
            monkey["counter"] += 1
            # operation
            op, n1, n2 = monkey["operation"]
            if n1 == "old":
                n1 = worryval
            if n2 == "old":
                n2 = worryval
            if op == "+":
                newworry = int(n1) + int(n2)
            if op == "*":
                newworry = int(n1) * int(n2)

            # bored
            # part1
            # boredworry = (newworry // 3) % divisor
            # part 2
            boredworry = newworry % divisor

            # print(worryval, newworry, boredworry)

            # test
            # print(monkey["test"], newworry % monkey["test"], 2080, 13, 2080 % 13)
            testresult = not (boredworry % (monkey["test"]))
            # print(worryval, newworry, boredworry, testresult)
            newmonkey = monkey[testresult]
            # print(worryval, newworry, boredworry, testresult, newmonkey)

            # throw
            monkeys[monkey[testresult]]["items"].append(boredworry)

        monkey["items"] = []

    if mround == 19:
        print([(i, m["counter"]) for i, m in enumerate(monkeys)])
        s1, s2 = sorted([m["counter"] for m in monkeys])[-2:]
        print(s1 * s2)

    if not (mround % 1000):
        print([(i, m["counter"]) for i, m in enumerate(monkeys)])


print([(i, m["counter"]) for i, m in enumerate(monkeys)])
s1, s2 = sorted([m["counter"] for m in monkeys])[-2:]
print(s1 * s2)
