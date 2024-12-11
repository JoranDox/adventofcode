

defmodule Puzzleday10 do
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

    defp info(msg, opts, force\\false) do
        log_level = System.get_env("LOG_LEVEL")
        if log_level in ["info", "debug"] or force do
            default_opts = [pretty: true, charlists: :as_lists]
            combined_opts = Keyword.merge(default_opts, opts)
            IO.inspect(msg, combined_opts)
        else
            msg
        end
    end

    def testinput do
        read_input("input/2024/day10inputtest.txt")
    end
    def testinput2 do
        read_input("input/2024/day10inputtest2.txt")
    end
    def realinput do
        read_input("input/2024/day10input.txt")
    end

    def tomap(list) do
        list
        |> Enum.with_index()
        |> Enum.map( fn {line, yindex} ->
            line
            |> Enum.with_index()
            |> debug(label: "read_input 4")
            |> Enum.map( fn {char, xindex} ->
                case char do
                    "." -> nil
                    node -> [{{xindex, yindex}, String.to_integer(node)}]
                end
                |> debug(label: "read_input 5")
            end)
        end)
        |> List.flatten()
        |> Enum.filter(fn x -> x != nil end)
        |> Map.new()
    end

    def mapsetbounds(mapset) do
        mapset
        # |> debug(label: "mapsetbounds 0")
        |> Enum.map(&Tuple.to_list/1)
        # |> debug(label: "mapsetbounds 1")
        |> Enum.zip()
        # |> debug(label: "mapsetbounds 2")
        |> Enum.map(&Tuple.to_list/1)
        # |> debug(label: "mapsetbounds 3")
        |> Enum.map(&Enum.max/1)
        # |> debug(label: "mapsetbounds 4")
    end

    def bounds(map) do
        Map.keys(map)
        # |> debug(label: "bounds 1")
        |> List.flatten()
        # |> debug(label: "bounds 2")
        |> mapsetbounds()
        # |> debug(label: "bounds 3")
    end

    def twodeeviz(map, force\\false) do
        [maxx, maxy] = bounds(map)
        log_level = System.get_env("LOG_LEVEL")
        if log_level in ["debug", "info"] or force do
            Enum.reduce(0..maxy, "", fn y, _acc ->
                Enum.reduce(0..maxx, "", fn x, acc2 ->
                    case map[{x,y}] do
                        nil -> acc2 <> " "
                        other -> acc2 <> "#{other}"
                    end
                end)
                |> info([label: "twodeeviz 1"], force)
            end)
        end
        info("", [label: "twodeeviz 2"], force)
        map
    end

    def read_input(filename) do
        File.read!(filename)
        |> String.split("\n", trim: true)
        |> debug(label: "read_input 1")
        |> Enum.map(fn line -> line |> String.split("", trim: true) end)
        |> debug(label: "read_input 2")

        |> debug(label: "read_input 3")
        |> tomap()
        |> debug(label: "read_input 4")
        |> twodeeviz()
        |> debug(label: "read_input 5")
    end

    def find(map, num) do
        map
        |> Map.filter(fn {{x,y}, value} -> value == num end)
        |> debug(label: "find #{num} 1")
        |> Map.keys()
        |> debug(label: "find #{num} 2")
    end

    def neighbours({x,y}, map, target) do
        [
            {x-1, y},
            {x+1, y},
            {x, y-1},
            {x, y+1}
        ]
    end

    def bfs(map, {fromx, fromy}, 9, path) do
        [{fromx, fromy} | path]
    end
    def bfs(map, {fromx, fromy}, fromn, path) do
        neighbours({fromx, fromy}, map, fromn+1)
        |> debug(label: "bfs #{fromn} 0")
        |> Enum.filter(fn neighbour -> map[neighbour] == (fromn+1) end) # only valid neighbours
        |> debug(label: "bfs #{fromn} 1")
        |> Enum.map(fn neighbour ->
            bfs(map, neighbour, fromn+1, [{fromx, fromy}|path])
        end)
        |> debug(label: "bfs #{fromn} 2") # this should be a list of lists of paths
        # |> Enum.any?(fn x -> x end) # part 1
        # |> Enum.map(fn x -> if x, do: 1, else: 0 end)
        # |> Enum.sum() # part 2
    end

    def canfindpath?(paths, {zerox, zeroy}, {ninex, niney}) do

    end

    def common(map) do
        map
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        # |> Enum.map(fn line -> {line, todo1(line)} end)
        |> debug(label: "run2")
        |> find(0)
        # |> Enum.count(fn {_line, sl} -> sl end)
        |> debug(label: "run3")
        |> Enum.map(fn zero ->
            {
                zero,
                bfs(map, zero, 0, [])
                |> debug(label: "run4")
                |> List.flatten()
                |> debug(label: "run5")
                |> Enum.chunk_every(10)
                |> debug(label: "run6")
            }
        end)
        # returns the list of paths per zero
    end

    def runpart1(map) do
        map
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        # |> Enum.map(fn line -> {line, todo1(line)} end)
        |> common()
        |> debug(label: "run7")
        |> Enum.map(fn {zero, pathlist} ->
            map
            |> find(9)
            |> debug(label: "run10, (these are all the nines)")
            |> MapSet.new()
            |> debug(label: "run11 (nines as set)")
            |> MapSet.intersection(
                pathlist
                |> List.flatten()
                |> MapSet.new()
            )
            |> debug(label: "run12 (intersection of nines and paths)")
            |> Enum.count()
            |> debug(label: "run13 (count of intersections)")
            # |> then(fn x ->
            #     case x do
            #         0 -> 0
            #         _ -> 1
            #     end
            # end)
        end)
        |> Enum.sum()
        # |> Enum.filter(fn {from, to, x} -> x end)
        # |> debug(label: "run8")
        # |> Enum.count()
        # |> debug(label: "run9")
    end

    def runpart2(map) do
        map
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        # |> Enum.map(fn line -> {line, todo1(line)} end)
        |> common()
        |> debug(label: "run7")
        |> Enum.map(fn {zero, pathlist} ->
            # {zero, length(pathlist)}
            # |> info(label: "run8 (sum these for part 2)")
            length(pathlist)
        end)
        |> Enum.sum()

    end
end

Puzzleday10.testinput()
|> Puzzleday10.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzleday10.testinput2()
|> Puzzleday10.runpart1()
|> IO.inspect(pretty: true, label: "testinput2, part1")

Puzzleday10.realinput()
|> Puzzleday10.runpart1()
|> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday10.testinput()
|> Puzzleday10.runpart2()
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday10.realinput()
|> Puzzleday10.runpart2()
|> IO.inspect(pretty: true, label: "realinput, part2")
