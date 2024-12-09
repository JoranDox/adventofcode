


defmodule Puzzleday07 do
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

    def testinput do
        read_input("input/2024/day07inputtest.txt")
    end

    def realinput do
        read_input("input/2024/day07input.txt")
    end

    def read_input(filename) do
        File.read!(filename)
        |> String.split("\n", trim: true)
        |> debug(label: "read_input 1")
        |> Enum.map(fn line ->
            line
            |> debug(label: "read_input 1.1")
            |> String.split(":", trim: true)
            |> debug(label: "read_input 1.2")
            |> then(fn [result, numbers] ->
                {
                    String.to_integer(result)
                    |> debug(label: "read_input 1.2.1"),
                    String.split(numbers)
                    |> debug(label: "read_input 1.2.2")
                    |> Enum.map(&String.to_integer/1)
                }
            end)
            |> debug(label: "read_input 1.3")
        end)
        |> debug(label: "read_input 2")
    end

    def checktest(result, _, accum, straccum) when accum > result do {false, ""} end
    def checktest(result, [], accum, straccum) do {result == accum, straccum} end
    def checktest(result, [head | numbers]) do
        checktest(result, numbers, head, "#{head}")
    end
    def checktest(result, [head | numbers], accum, straccum) do
        {b1, accum1} = checktest(result, numbers, head + accum, straccum <> " + #{head}")
        if b1 do
            {b1, accum1}
        else
            {b2, accum2} = checktest(result, numbers, head * accum, straccum <> " * #{head}")
            if b2 do
                {b2, accum2}
            else
                # comment this part out for part 1 I guess
                {b3, accum3} = checktest(result, numbers, String.to_integer("#{accum}#{head}"), straccum <> " || #{head}")
                if b3 do
                    {b3, accum3}
                else
                    {false, ""}
                end
            end
        end
    end



    def runpart1(input) do
        input
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        |> Enum.map(fn {result, numbers} -> {result, numbers, checktest(result, numbers)} end)
        |> debug(label: "run2")
        |> Enum.map(fn {result, _, {bool, _}} -> if bool do result else 0 end end)
        |> debug(label: "run3")
        |> Enum.sum()
        |> debug(label: "run4")
    end

    def runpart2(input) do
        input
        # |> Enum.map(fn line -> {line, todo2(line)} end)
        |> debug(label: "run2")
        # |> Enum.count(fn {_line, sl} -> sl end)
        |> debug(label: "run3")
    end
end

Puzzleday07.testinput()
|> Puzzleday07.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzleday07.realinput()
|> Puzzleday07.runpart1()
|> IO.inspect(pretty: true, label: "realinput, part1")

# Puzzleday07.testinput()
# |> Puzzleday07.runpart2()
# |> IO.inspect(pretty: true, label: "testinput, part2")

# Puzzleday07.realinput()
# |> Puzzleday07.runpart2()
# |> IO.inspect(pretty: true, label: "realinput, part2")
