import os
import pathlib

currentyear = 2024
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
    elixirname = basename + ".exs"

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
    if elixirname not in existing and not dry_run:
        with open(solution_dir.joinpath(elixirname), "w") as f:
            f.write(
                f"""

defmodule Part1 do
    def run do
        # File.read!("input/{str(currentyear)}/{basename}inputtest.txt")
        File.read!("input/{str(currentyear)}/{basename}input.txt")

        |> String.split("\\n")
        |> IO.inspect(pretty: true)
    end
end

defmodule Part2 do
    def run do
        # File.read!("input/2024/day01inputtest.txt")
        File.read!("input/2024/day01input.txt")

        |> String.split("\\n")
        |> IO.inspect(pretty: true)

    end
end

Part1.run()
#Part2.run()
"""
            )
        with open(input_dir.joinpath(basename + "inputtest.txt"), "w") as f:
            pass  # touch file
        with open(input_dir.joinpath(basename + "input.txt"), "w") as f:
            pass  # touch file
        break
