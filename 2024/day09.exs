
require Integer



defmodule Puzzleday09 do
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

    defp printabledisk([]) do
        ""
    end
    defp printabledisk([head | rest]) do
        "#{head}" <> printabledisk(rest)
    end

    defp debugdisk(disk, opts) do
        log_level = System.get_env("LOG_LEVEL")
        if log_level == "debug" do
            default_opts = [pretty: true, charlists: :as_lists]
            combined_opts = Keyword.merge(default_opts, opts)
            disk
            |> densetosparse()
            |> Enum.reverse()
            |> printabledisk()
            |> IO.inspect(combined_opts)
        end
        disk
    end

    def testinput do
        read_input("input/2024/day09inputtest.txt")
    end

    def realinput do
        read_input("input/2024/day09input.txt")
    end

    def chompdots([]) do
        []
    end
    def chompdots(["." | rest]) do
        chompdots(rest)
    end
    def chompdots([head | rest]) do
        [head | rest]
    end

    def fragsort([]) do
        debug([], label: "fragsort degen")
        []
    end
    def fragsort(["." | tail]) do
        debug(["." | tail], label: "fragsort dot in")
        # find last non-dot element
        chompedreversedlist = Enum.reverse(tail) |> chompdots()
        |> debug(label: "fragsort dot 1")
        case chompedreversedlist do
            [] -> [] |> debug(label: "fragsort dot degen")
            [last] -> [last] |> debug(label: "fragsort dot last")
            [last | rest] -> [last | fragsort(Enum.reverse(rest))]
        end
        |> debug(label: "fragsort dot out")
    end
    def fragsort([head | tail]) do
        debug([head | tail], label: "fragsort head in")
        [head | fragsort(tail)]
        |> debug(label: "fragsort head out")
    end

    def insertfile([], file) do
        [file]
    end
    def insertfile([{:empty, count} | tail], {:file, filecount, filevalue}) when count == filecount do
        [{:file, filecount, filevalue} | tail] ++ [{:empty, filecount}]
    end
    def insertfile([{:empty, count} | tail], {:file, filecount, filevalue}) when count > filecount do
        [{:file, filecount, filevalue}, {:empty, count - filecount} | tail] ++ [{:empty, filecount}]
    end
    def insertfile([head | tail], file) do
        [head | insertfile(tail, file)]
    end

    def defrag(list) do
        revlist = Enum.reverse(list)
        debugdisk(revlist, label: "defrag in")
        # assert we definitely have a head that is a file
        [{:file, _count, value} | _rest] = revlist
        # now defrag starting with the index of the last element
        defragsort(revlist, value)
        |> debugdisk(label: "defrag out")
        |> Enum.reverse()
        |> debugdisk(label: "defrag out reversed")

    end
    def defragsort([], _index) do
        []
    end
    def defragsort([head | tail], index) do
        # find first (=last because list is reversed) big enough hole to fit the head
        debug(index, label: "defragsort in, index")
        debugdisk([head | tail], label: "defragsort in, list")
        case head do
            {:file, _count, ^index} -> Enum.reverse(insertfile(Enum.reverse(tail), head))
                |> debugdisk(label: "defragsort 1")
                |> defragsort(index-1)
            _ -> [head | defragsort(tail, index)] |> debugdisk(label: "defragsort skip")
        end
        |> debugdisk(label: "defragsort out")
    end


    def tobetterdense(list, index \\ 0)
    def tobetterdense([], _index) do
        []
    end
    def tobetterdense([0 | rest], index) do
        tobetterdense(rest, index + 1)
    end
    def tobetterdense([head | rest], index) when Integer.is_even(index) do
        [{:file, head, div(index,2)} | tobetterdense(rest, index + 1)]
    end
    def tobetterdense([head | rest], index) when Integer.is_odd(index) do
        [{:empty, head} | tobetterdense(rest, index + 1)]
    end

    def densetosparse([]) do
        []
    end
    def densetosparse([head | tail]) do
        case head do
            {:file, count, value} -> (for _ <- 1..count, do: value) ++ densetosparse(tail)
            {:empty, count} -> (for _ <- 1..count, do: ".") ++ densetosparse(tail)
        end
    end

    def read_input(filename) do
        File.read!(filename)
        |> String.split("", trim: true)
        |> debug(label: "read_input 1")
        |> Enum.map(&String.to_integer/1)
        |> debug(label: "read_input 2")
    end

    def score(line, index \\ 0)
    def score([], _index) do
        0
    end
    def score(["." | tail], index) do
        score(tail, index + 1)
    end
    def score([head | tail], index) do
        head * index + score(tail, index + 1)
    end

    def runpart1(input) do
        input
        |> tobetterdense()
        |> densetosparse()
        |> debug(label: "run1")
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        |> fragsort()
        |> debug(label: "run2")
        |> score()
        |> debug(label: "run3")
    end

    def runpart2(input) do
        input
        |> tobetterdense()
        |> debug(label: "run1")
        # |> Enum.map(fn line -> {line, todo2(line)} end)
        |> defrag()
        |> debug(label: "run2")
        |> densetosparse()
        |> debug(label: "run3")
        |> score()
        |> debug(label: "run4")
    end
end

Puzzleday09.testinput()
|> Puzzleday09.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")
IO.puts("")

# Puzzleday09.realinput()
# |> Puzzleday09.runpart1()
# |> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday09.testinput()
|> Puzzleday09.runpart2()
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday09.realinput()
|> Puzzleday09.runpart2()
|> IO.inspect(pretty: true, label: "realinput, part2")
