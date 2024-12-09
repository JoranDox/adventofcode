


defmodule Puzzleday08 do
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

    def twodeeviz(nodes, map, force\\false) do
        [maxx, maxy] = bounds(map)
        log_level = System.get_env("LOG_LEVEL")
        if log_level in ["debug", "info"] or force do
            Enum.reduce(0..maxy, "", fn y, _acc ->
                Enum.reduce(0..maxx, "", fn x, acc2 ->
                    if {x,y} in nodes do
                        acc2 <> "#"
                    else
                        acc2 <> " "
                    end
                end)
                |> info([label: "twodeeviz 1"], force)
            end)
        end
        info("", [label: "twodeeviz 2"], force)
        nodes
    end

    def testinput do
        read_input("input/2024/day08inputtest.txt")
    end

    def realinput do
        read_input("input/2024/day08input.txt")
    end

    def bounds(map) do
        Map.values(map)
        |> debug(label: "bounds 1")
        |> List.flatten()
        |> debug(label: "bounds 2")
        |> mapsetbounds()
    end

    def mapsetbounds(mapset) do
        mapset
        |> debug(label: "mapsetbounds 0")
        |> Enum.map(&Tuple.to_list/1)
        |> debug(label: "mapsetbounds 1")
        |> Enum.zip()
        |> debug(label: "mapsetbounds 2")
        |> Enum.map(&Tuple.to_list/1)
        |> debug(label: "mapsetbounds 3")
        |> Enum.map(&Enum.max/1)
        |> debug(label: "mapsetbounds 4")
    end

    def inbounds?({x,y}, maxx, maxy) do
        x >= 0 and x <= maxx and y >= 0 and y <= maxy
    end

    def checkbounds(antinodes, map) do
        [maxx, maxy] = bounds(map)
        antinodes
        |> debug(label: "checkbounds 0")
        |> Enum.filter(fn {x,y} -> inbounds?({x,y}, maxx, maxy) end)
        |> debug(label: "checkbounds 1")
    end

    def read_input(filename) do
        File.read!(filename)
        |> debug(label: "read_input 0")
        |> String.split("\n", trim: true)
        |> debug(label: "read_input 1")
        |> Enum.map(fn line -> line |> String.split("", trim: true) end)
        |> debug(label: "read_input 2")
        |> Enum.with_index()
        |> debug(label: "read_input 3")
        |> Enum.map( fn {line, yindex} ->
            line
            |> Enum.with_index()
            |> debug(label: "read_input 4")
            |> Enum.map( fn {char, xindex} ->
                case char do
                    "." -> nil
                    node -> [{node, {xindex, yindex}}]
                end
                |> debug(label: "read_input 5")
            end)
        end)
        |> debug(label: "read_input 6")
        |> List.flatten()
        |> debug(label: "read_input 7")
        |> Enum.filter(fn x -> x != nil end)
        |> debug(label: "read_input 8")
        |> Enum.reduce(%{}, fn {key, value}, acc -> Map.put(acc, key, [value | Map.get(acc, key, [])]) end)
        |> debug(label: "read_input 9")
    end

    def product([], accum, _seen) do
        debug({[], accum, _seen}, label: "product end 1")
        accum
        |> debug(label: "product end 2")
    end
    def product([head]) do
        debug({[head]}, label: "product start degenerate 1")
        []
        |> debug(label: "product start degenerate 2")
    end
    def product([head | rest]) do
        debug({[head | rest]}, label: "product start 1")
        product(rest, [], [head])
        |> debug(label: "product start 2")
    end
    def product([head | rest], accum, seen) do
        debug({[head | rest], accum, seen}, label: "product 1.1")
        product(
            rest,
            Enum.map(seen, fn node -> {head, node} end) ++ accum,
            [head | seen]
        )
        |> debug(label: "product 1.2")
    end
    # c "2024/day08.exs"
    # Puzzleday08.product([1,2,3])

    def linterp(x1, x2) do
        if x2 < x1 do
            {newx1, newx2} = linterp(x2, x1)
            {newx2, newx1}
        else
            {x1 - (x2-x1), x2 + (x2-x1)}
        end
    end

    def oneantinodepair({{x1,y1}, {x2,y2}}) do
        {newx1, newx2} = linterp(x1, x2)
        {newy1, newy2} = linterp(y1, y2)
        [
            {newx1, newy1},
            {newx2, newy2}
        ]
    end

    def lineextendleft(accum, {xdiff, ydiff}, {maxx, maxy}) do
        [{x1, y1} | rest] = accum
        if inbounds?({x1, y1}, maxx, maxy) do
            lineextendleft([{x1-xdiff, y1-ydiff} | accum], {xdiff, ydiff}, {maxx, maxy})
        else
            accum
        end
    end

    def getline({{x1,y1}, {x2,y2}}, map) do
        [maxx, maxy] = bounds(map)
        xdiff = x2-x1
        ydiff = y2-y1
        gcd = Integer.gcd(xdiff, ydiff)
        xdiff = div(xdiff, gcd)
        ydiff = div(ydiff, gcd)
        leftline = lineextendleft([{x1, y1}], {xdiff, ydiff}, {maxx, maxy})
        |> debug(label: "getline left")
        rightline = lineextendleft([{x1, y1}], {-xdiff, -ydiff}, {maxx, maxy})
        |> debug(label: "getline right")
        MapSet.to_list(MapSet.new(List.flatten([
            leftline,
            rightline
        ])))
    end

    def antinodes(map) do
        map
        |> Enum.map(fn {node, coords} ->
            debug({node, coords}, label: "antinodes 0")
            # {
                # node,
                coords
                |> product()
                |> debug(label: "antinodes 1")
                |> Enum.map(&oneantinodepair/1)
                |> debug(label: "antinodes 2")
            # }
        end)
        |> debug(label: "antinodes 3")
        |> List.flatten()
        |> debug(label: "antinodes 4")
        |> MapSet.new()
        |> debug(label: "antinodes 5")
    end

    def antinodes2(map) do
        map
        |> Enum.map(fn {node, coords} ->
            debug({node, coords}, label: "antinodes 0")
            # {
                # node,
                coords
                |> product()
                |> debug(label: "antinodes 1")
                |> Enum.map(fn loc -> getline(loc, map) end)
                |> debug(label: "antinodes 2")
            # }
        end)
        |> debug(label: "antinodes 3")
        |> List.flatten()
        |> debug(label: "antinodes 4")
        |> MapSet.new()
        |> debug(label: "antinodes 5")
    end

    def runpart1(input) do
        input
        |> debug(label: "run1")
        |> antinodes()
        |> debug(label: "run2")
        |> checkbounds(input)
        |> debug(label: "run3")
        |> length()
        |> debug(label: "run4")
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        # # |> Enum.map(fn line -> {line, todo1(line)} end)
        # |> debug(label: "run2")
        # |> Enum.count(fn {_line, sl} -> sl end)
        # |> debug(label: "run3")
    end

    def runpart2(input) do
        input
        |> debug(label: "run1")
        |> antinodes2()
        |> debug(label: "run2")
        |> twodeeviz(input)
        |> checkbounds(input)
        |> debug(label: "run3")
        |> length()
        |> debug(label: "run4")
    end
end

Puzzleday08.testinput()
|> Puzzleday08.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzleday08.realinput()
|> Puzzleday08.runpart1()
|> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday08.testinput()
|> Puzzleday08.runpart2()
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday08.realinput()
|> Puzzleday08.runpart2()
|> IO.inspect(pretty: true, label: "realinput, part2")
