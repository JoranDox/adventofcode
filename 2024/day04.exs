


defmodule Puzzleday04 do
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
        read_input("input/2024/day04inputtest.txt")
    end

    def realinput do
        read_input("input/2024/day04input.txt")
    end

    def pad(lines) do
        lines
        |> padlines
        # |> zip
        # |> padlines
        # |> zip
    end

    def padlines(lines) do
        lines
        |> Enum.map(fn line -> line ++ [".", ".", "."] end)

    end

    def read_input(filename) do
        File.read!(filename)
        |> debug(label: "read_input 0")
        |> String.split("\n", trim: true)
        |> debug(label: "read_input 1")
        |> Enum.map(fn line -> String.split(line, "", trim: true) end)
        |> debug(label: "read_input 2")
        |> pad()
        # |> padlines()
        |> debug(label: "read_input 3")
        |> Enum.zip()
        |> debug(label: "read_input 4")
        |> Enum.map(&Tuple.to_list/1)
        |> debug(label: "read_input 5")
        |> pad()
        |> debug(label: "read_input 6")
        |> Enum.zip()
        |> Enum.map(&Tuple.to_list/1)
        |> debug(label: "read_input 7")


    end

    def split_again(lines) do
        lines
        |> debug(label: "split_again 0")
        |> debug(label: "split_again 1")
        |> Enum.zip()
        |> debug(label: "split_again 2")
    end

    def stop(input) do
    end

    def counthor(square) do
        case square do
            [["X", "M", "A", "S"], _, _, _] -> 1
            [["S", "A", "M", "X"], _, _, _] -> 1
            _ -> 0
        end
    end

    def countvert(square) do
        case square do
            [["X", _, _, _], ["M", _, _, _], ["A", _, _, _], ["S", _, _, _]] -> 1
            [["S", _, _, _], ["A", _, _, _], ["M", _, _, _], ["X", _, _, _]] -> 1
            _ -> 0
        end
    end

    def countdiag(square) do
        case square do
            [["X", _, _, _], [_, "M", _, _], [_, _, "A", _], [_, _, _, "S"]] -> 1
            [["S", _, _, _], [_, "A", _, _], [_, _, "M", _], [_, _, _, "X"]] -> 1
            _ -> 0
        end
    end

    def countantidiag(square) do
        case square do
            [[_, _, _, "X"], [_, _, "M", _], [_, "A", _, _], ["S", _, _, _]] -> 1
            [[_, _, _, "S"], [_, _, "A", _], [_, "M", _, _], ["X", _, _, _]] -> 1
            _ -> 0
        end
    end

    def countxmas(square) do
        countvert(square) + counthor(square) + countdiag(square) + countantidiag(square)
    end

    def count_x_mas(square) do
        case square do
            [["M", _, "M"], [_, "A", _], ["S", _, "S"]] -> 1
            [["M", _, "S"], [_, "A", _], ["M", _, "S"]] -> 1
            [["S", _, "S"], [_, "A", _], ["M", _, "M"]] -> 1
            [["S", _, "M"], [_, "A", _], ["S", _, "M"]] -> 1
            _ -> 0
        end
    end

    def shared(input, num) do


        input
        |> Enum.chunk_every(num, 1, :discard)
        |> debug(label: "run1")
        # |> Enum.map(&split_again/1)
        |> Enum.map(&Enum.zip/1)
        |> debug(label: "run2")
        |> Enum.map(fn line -> Enum.chunk_every(line, num, 1, :discard) end)
        |> debug(label: "run3")
        # untuple the zip
        |> Enum.map(fn listofsquares ->
            listofsquares
            |> Enum.map(fn square ->
                square
                |> Enum.map(&Tuple.to_list/1)
            end)
        end)
    end

    def runpart1(input) do
        input
        |> shared(4)
        |> Enum.map(fn listofsquares ->
            listofsquares
            |> Enum.map(fn square -> countxmas(square) end)
        end)
        |> debug(label: "run4")
        |> Enum.map(fn squareofscores ->
            squareofscores
            |> Enum.sum()
        end)
        |> debug(label: "run5")
        |> Enum.sum()
        |> debug(label: "run6")
        # |> Enum.count
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        # |> Enum.map(fn line -> {line, todo1(line)} end)
        # |> Enum.count(fn {_line, sl} -> sl end)
    end

    def runpart2(input) do
        input
        |> shared(3)
        |> Enum.map(fn listofsquares ->
            listofsquares
            |> Enum.map(fn square -> count_x_mas(square) end)
        end)
        |> debug(label: "run4")
        |> Enum.map(fn squareofscores ->
            squareofscores
            |> Enum.sum()
        end)
        |> debug(label: "run5")
        |> Enum.sum()
        |> debug(label: "run6")
    end
end

Puzzleday04.testinput()
|> Puzzleday04.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzleday04.realinput()
|> Puzzleday04.runpart1()
|> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday04.testinput()
|> Puzzleday04.runpart2()
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday04.realinput()
|> Puzzleday04.runpart2()
|> IO.inspect(pretty: true, label: "realinput, part2")
