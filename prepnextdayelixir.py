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
        testfilename = basename + "inputtest.txt"
        realfilename = basename + "input.txt"
        with open(solution_dir.joinpath(elixirname), "w") as f:
            f.write(
                f"""


defmodule Puzzle{basename} do
    defp debug(msg, opts) do
        log_level = System.get_env("LOG_LEVEL")
        if log_level == "debug" do
            default_opts = [pretty: true, charlists: :as_lists]
            combined_opts = Keyword.merge(default_opts, opts)
            IO.inspect(msg, combined_opts)
        else
            msg
        end
    end

    def read_input(filename) do
        File.read!(filename)
        |> String.split("\\n", trim: true)
        |> debug(label: "read_input 1")
        |> Enum.map(&String.split/1)
        |> debug(label: "read_input 2")
        |> Enum.map(
            fn line -> Enum.map(line, &String.to_integer/1) end
        )
        |> debug(label: "read_input 3")
    end

    def runpart1(input) do
        input
        |> Task.async_stream(fn line -> {{line, todo1(line)}} end)
        |> Enum.map(fn {{:ok, result}} -> result end)
        # |> Enum.map(fn line -> {{line, todo1(line)}} end)
        |> debug(label: "run2")
        |> Enum.count(fn {{_line, sl}} -> sl end)
        |> debug(label: "run3")
    end

    def runpart2(input) do
        input
        |> Enum.map(fn line -> {{line, todo2(line)}} end)
        |> debug(label: "run2")
        |> Enum.count(fn {{_line, sl}} -> sl end)
        |> debug(label: "run3")
    end
end


Puzzle{basename}.read_input("input/{currentyear}/{testfilename}")
|> Puzzle{basename}.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzle{basename}.read_input("input/{currentyear}/{realfilename}")
|> Puzzle{basename}.runpart1()
|> IO.inspect(pretty: true, label: "realinput, part1")

Puzzle{basename}.read_input("input/{currentyear}/{testfilename}")
|> Puzzle{basename}.runpart2()
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzle{basename}.read_input("input/{currentyear}/{realfilename}")
|> Puzzle{basename}.runpart2()
|> IO.inspect(pretty: true, label: "realinput, part2")

"""
            )
        if testfilename not in os.listdir(input_dir):
            with open(input_dir.joinpath(testfilename), "w") as f:
                pass  # touch file
        if realfilename not in os.listdir(input_dir):
            with open(input_dir.joinpath(realfilename), "w") as f:
                pass  # touch file
        break

