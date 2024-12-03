


defmodule Puzzleday03 do
    defp debug(msg, opts \\ []) do
        default_opts = [pretty: true, charlists: :as_lists]
        combined_opts = Keyword.merge(default_opts, opts)
        IO.inspect(msg, combined_opts)
        # msg
    end


    def testinput do
        read_input("input/2024/day03inputtest.txt")
    end

    def realinput do
        read_input("input/2024/day03input.txt")
    end

    def read_input(filename) do
        File.read!(filename)
        # |> String.split("\n", trim: true)
        |> debug(label: "read_input 1")
    end

    def runpart1(input) do
        regex = ~r/mul\((\d+),(\d+)\)/
        input
        |> debug(label: "run0")
        |> then(fn string -> Regex.scan(regex, string) end)
        |> debug(label: "run1")
        |> Enum.map(fn [_, a, b] -> String.to_integer(a) * String.to_integer(b) end)
        |> debug(label: "run2")
        |> Enum.sum()
        |> debug(label: "run3")

    end

    defp do_or_dont(string) do
        case string do
            "do()" <> rest -> runpart1(rest)
            "don't()" <> rest -> 0
            rest -> runpart1(rest)
        end
    end

    def runpart2(input) do
        regex_do_or_dont = ~r/(?=do(n't)?\(\))/
        input
        |> debug(label: "run0")
        |> then(fn string -> Regex.split(regex_do_or_dont, string) end)
        |> debug(label: "run1")
        |> Enum.map(&do_or_dont/1)
        |> debug(label: "run2")
        |> Enum.sum()
        |> debug(label: "run3")
    end
end

Puzzleday03.testinput()
|> Puzzleday03.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzleday03.realinput()
|> Puzzleday03.runpart1()
|> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday03.testinput()
|> Puzzleday03.runpart2()
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday03.realinput()
|> Puzzleday03.runpart2()
|> IO.inspect(pretty: true, label: "realinput, part2")
