import os
import pathlib

currentyear = 2025
dry_run = False
path = pathlib.Path(__file__).resolve().absolute()
print(path, type(path))

aoc_dir = path.parent
print("aoc_dir:", aoc_dir)

input_dir = aoc_dir.joinpath(f"input/{str(currentyear)}")
print("input_dir:", input_dir)
solution_dir = aoc_dir.joinpath(str(currentyear))
print("solution_dir:", solution_dir)
existing = os.listdir(solution_dir)
print(existing)

for day in range(1, 26):
    basename = f"day{str(day).zfill(2)}"
    pyname = basename + ".py"

    # print(solution_dir.joinpath(pyname))
    # print(input_dir.joinpath(basename + "inputtest.txt"))
    # print(f'aoc_dir.joinpath("input/{str(currentyear)}/{basename}inputtest.txt")')
    # print(input_dir.joinpath(basename + "input.txt"))
    # print(f'aoc_dir.joinpath(f"input/{str(currentyear)}/{basename}input.txt")')
    #     print(f"""
    # import pathlib
    # aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
    # #with open(aoc_dir.joinpath("input/{str(currentyear)}/{basename}inputtest.txt")) as f:
    # with open(aoc_dir.joinpath("input/{str(currentyear)}/{basename}input.txt")) as f:
    #     data = f.read().strip()
    # """)
    if pyname not in existing and not dry_run:
        with open(solution_dir.joinpath(pyname), "w") as f:
            f.write(
                f"""
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
with open(aoc_dir.joinpath("input/{str(currentyear)}/{basename}inputtest.txt")) as f:
# with open(aoc_dir.joinpath("input/{str(currentyear)}/{basename}input.txt")) as f:
    data = f.read().strip()

for line in data.splitlines():
#for line in data.split("\\n\\n"):


"""
            )
        print("Created solution file:", solution_dir.joinpath(pyname))
        testfilename = basename + "inputtest.txt"
        realfilename = basename + "input.txt"
        if testfilename not in os.listdir(input_dir):
            with open(input_dir.joinpath(testfilename), "w") as f:
                pass  # touch file
            print("Created test file:", input_dir.joinpath(testfilename))
        if realfilename not in os.listdir(input_dir):
            with open(input_dir.joinpath(realfilename), "w") as f:
                pass  # touch file
            print("Created real file:", input_dir.joinpath(realfilename))
        break
