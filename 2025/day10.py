import pathlib
import itertools
import z3

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2025/day10inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2025/day10input.txt")) as f:
    data = f.read().strip()


def modsumtuples(*t: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(x) % 2 for x in zip(*t))


def sumtuples(*t: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(x) for x in zip(*t))


totalcost = 0
totalcostp2 = 0
for line in data.splitlines():
    rawtarget, *rawbuttons, rawcosts = line.split()

    assert rawtarget.startswith("[") and rawtarget.endswith("]")
    target = tuple([int(c == "#") for c in rawtarget[1:-1]])

    buttonindices: list[tuple[int, ...]] = [
        tuple(map(int, rb[1:-1].split(","))) for rb in rawbuttons
    ]
    buttons = [
        tuple([int(i in bi) for i in range(len(target))]) for bi in buttonindices
    ]

    print(target, buttons, rawcosts)
    found = False
    for i in range(len(buttons)):
        # try to get the solution in i button presses before trying more
        for bis in itertools.combinations(range(len(buttons)), i):
            bs = [buttons[b] for b in bis]

            print(target, bis, bs, modsumtuples(*bs))
            if modsumtuples(*bs) == tuple(target):
                totalcost += i
                print("found solution with", i, "buttons:", bs)
                found = True
                break

        if found:
            break

    # part 2 in z3
    target2 = tuple(map(int, rawcosts[1:-1].split(",")))
    # optimise minimal button presses
    # the buttons now add instead of toggling
    solver = z3.Optimize()
    button_vars = [z3.Int(f"b{i}") for i in range(len(buttons))]
    for bv in button_vars:
        solver.add(bv >= 0)
    for i in range(len(target2)):
        solver.add(
            sum(button_vars[j] * buttons[j][i] for j in range(len(buttons)))
            == target2[i]
        )

    h = solver.minimize(sum(button_vars))
    # we know there's a solution
    assert solver.check() == z3.sat
    model = solver.model()
    cost = sum(model[bv].as_long() for bv in button_vars)
    totalcostp2 += cost

print("part 1 cost", totalcost)
print("part 2 cost:", totalcostp2)
