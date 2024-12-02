

defmodule Day02 do
    defp debug(msg, opts \\ []) do
        # default_opts = [pretty: true, charlists: :as_lists]
        # combined_opts = Keyword.merge(default_opts, opts)
        # IO.inspect(msg, combined_opts)
        msg
    end

    defp monotonic?(list) do
        (Enum.sort(list, :asc) == list) || (Enum.sort(list, :desc) == list)
        |> debug(label: "monotonic")
    end


    defp noduplicates?(list) do
        Enum.uniq(list) == list
    end

    defp strictlymonotonic?(list) do
        monotonic?(list) && noduplicates?(list)
    end



    defp smalldifferences?(list) do
        Enum.chunk_every(list, 2, 1, :discard)
        |> debug(label: "smalldifferences1")
        |> Enum.map(fn [a,b] -> abs(a-b) <= 3 end)
        |> debug(label: "smalldifferences2")
        |> Enum.all?()
        |> debug(label: "smalldifferences3")
    end

    defp safeline(line) do
        line
        |> debug(label: "safeline2")
        |> then(fn l -> strictlymonotonic?(l) && smalldifferences?(l) end)
        |> debug(label: "safelineend")
    end

    defp dampened_safeline(line) do
        # leave one out per line
        line
        |> debug(label: "dampened_safeline0")
        |> Enum.with_index()
        |> debug(label: "dampened_safeline1")
        |> Enum.map(fn {l, i} -> {line, i} end)
        |> debug(label: "dampened_safeline2")
        |> Enum.map(fn {l, i} -> List.delete_at(l, i) end)
        |> debug(label: "dampened_safeline3")
        |> Enum.map(&safeline/1)
        |> Enum.any?
    end

    def testinput do
        read_input("input/2024/day02inputtest.txt")
    end

    def realinput do
        read_input("input/2024/day02input.txt")
    end

    def read_input(filename) do
        File.read!(filename)
        |> String.split("\n", trim: true)
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
        |> Task.async_stream(fn line -> {line, safeline(line)} end)
        |> Enum.map(fn {:ok, result} -> result end)
        # |> Enum.map(fn line -> {line, safeline(line)} end)
        |> debug(label: "run2")
        |> Enum.count(fn {_line, sl} -> sl end)
        |> debug(label: "run3")
    end


    def runpart2(input) do
        input
        |> Enum.map(fn line -> {line, dampened_safeline(line)} end)
        |> debug(label: "run2")
        |> Enum.count(fn {_line, sl} -> sl end)
        |> debug(label: "run3")
    end
end

Day02.testinput()
|> Day02.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")

Day02.realinput()
|> Day02.runpart1()
|> IO.inspect(pretty: true, label: "realinput, part1")

Day02.testinput()
|> Day02.runpart2()
|> IO.inspect(pretty: true, label: "testinput, part2")

Day02.realinput()
|> Day02.runpart2()
|> IO.inspect(pretty: true, label: "realinput, part2")
