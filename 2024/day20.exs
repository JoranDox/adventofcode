


defmodule Puzzleday20 do
    def debug(msg, opts) do
        log_level = System.get_env("LOG_LEVEL")
        if log_level == "debug" do
            default_opts = [pretty: true, charlists: :as_lists]
            combined_opts = Keyword.merge(default_opts, opts)
            IO.inspect(msg, combined_opts)
        else
            msg
        end
    end


    def info(msg, opts, force\\false) do
        log_level = System.get_env("LOG_LEVEL")
        if log_level in ["info", "debug"] or force do
            default_opts = [pretty: true, charlists: :as_lists]
            combined_opts = Keyword.merge(default_opts, opts)
            IO.inspect(msg, combined_opts)
        else
            msg
        end
    end

    defmodule Point2d do
        defstruct [:x, :y]
    end
    def point2dsum({x1,y1}, {x2,y2}) do
        {x1+x2, y1+y2}
    end
    def point2dsum({x, y}, :up) do {x, y-1} end
    def point2dsum({x, y}, :down) do {x, y+1} end
    def point2dsum({x, y}, :left) do {x-1, y} end
    def point2dsum({x, y}, :right) do {x+1, y} end
    def point2dsum({x, y}, :^) do {x, y-1} end
    def point2dsum({x, y}, :v) do {x, y+1} end
    def point2dsum({x, y}, :<) do {x-1, y} end
    def point2dsum({x, y}, :>) do {x+1, y} end
    def point2dsum(p1, p2) do
        %Point2d{x: p1.x + p2.x, y: p1.y + p2.y}
    end

    def mapsetbounds(mapset) do
        mapset
        # |> debug(label: "mapsetbounds 0", limit: :infinity)
        # |> Enum.map(fn p -> [p.x, p.y] end)
        |> Enum.map(fn {x, y} -> [x, y] end)
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
        |> Enum.filter(fn p -> (p != :end and p != :start) end)
        # |> debug(label: "bounds 1", limit: :infinity)
        |> mapsetbounds()
        # |> debug(label: "bounds 2")
    end

    def twodeeviz(map, force\\false) do
        # info(map, label: "twodeeviz map")
        [maxx, maxy] = bounds(map)
        log_level = System.get_env("LOG_LEVEL")
        if log_level in ["debug", "info"] or force do
            Enum.reduce(0..maxy, "", fn y, _acc ->
                Enum.reduce(0..maxx, "", fn x, acc2 ->
                    # case map[%Point2d{x: x,y: y}] do
                    case map[{x, y}] do
                        nil -> acc2 <> " "
                        :wall -> acc2 <> "#"
                        :start -> acc2 <> "S"
                        :end -> acc2 <> "E"
                        :path -> acc2 <> "X"
                        num -> acc2 <> Integer.to_string(div(num, 10))
                        # num -> acc2 <> Integer.to_string(div(num, 1000))

                        # nil -> acc2 <> "  "
                        # :wall -> acc2 <> "##"
                        # :start -> acc2 <> " S"
                        # :end -> acc2 <> " E"
                        # :path -> acc2 <> "><"
                        # num -> acc2 <> case num do
                        #     num when num < 10 -> "0" <> Integer.to_string(num)
                        #     num ->  Integer.to_string(num)
                        # end

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
        |> Enum.with_index()
        |> Enum.map(
            fn {line, y} ->
                line
                |> String.split("", trim: true)
                |> Enum.with_index()
                |> Enum.map(
                    fn {char, x} ->
                        case char do
                            "." -> nil
                            "#" -> {{x, y}, :wall}
                            "S" -> [
                                # {{x, y}, :start},
                                {:start, {x, y}}
                            ]
                            "E" -> [
                                # {{x, y}, :end}
                                # {:end, {x, y}}
                            ]
                        end
                    end
                )
            end
        )
        |> List.flatten()
        |> Enum.filter(fn x -> x != nil end)
        |> Map.new()
        # |> debug(label: "read_input map", limit: :infinity)
        |> Map.pop(:start)
        |> then(fn {start, poppedmap} -> (
            twodeeviz(poppedmap)
            {start, poppedmap}
        )end)
        |> then(fn {start, poppedmap} -> maptosteps(Map.put(poppedmap, start, 0), start, 1) end)
        |> twodeeviz()
    end

    def neighbours({x, y}) do
        # debug({x, y}, label: "neighbours")
        [{x, y-1}, {x, y+1}, {x-1, y}, {x+1, y}]
    end

    def maptosteps(map, pos, steps) do
        pos
        |> debug(label: "maptosteps in #{steps}")
        |> neighbours()
        # |> debug(label: "maptosteps neighbours #{steps}")
        # only new steps, instructions say there's only one path
        |> Enum.filter(fn p -> map[p] == nil end)
        |> Enum.reduce(map, fn p, acc -> maptosteps(Map.put(acc, p, steps), p, steps + 1) end)
        # |> debug(label: "maptosteps after recursion #{steps}")
    end

    def manhattandistance({x1, y1}, {x2, y2}) do
        abs(x1 - x2) + abs(y1 - y2)
    end

    def neighboursatmax({x,y}, maxrange) do
        (x-maxrange..x+maxrange)
        |> Enum.map(fn x2 ->
            (y-maxrange..y+maxrange)
            |> Enum.map(fn y2 -> {x2, y2} end)
        end)
        |> List.flatten()
        |> Enum.map(fn p -> {p, manhattandistance({x,y}, p)} end)
        |> Enum.filter(fn {_p, dist} -> dist <= maxrange end)
    end

    def vizcheat({{x1,y1}, {x2,y2}, saved}, map) do
        map
        |> Map.put({x1,y1}, :path)
        |> Map.put({x2,y2}, :path)
        # also the inbetween point
        |> Map.put({(x1+x2)/2, (y1+y2)/2}, :path)
        |> twodeeviz()
        {{x1,y1}, {x2,y2}, saved}
    end

    def findcheats({maptile, steps}, map, maxrange) do
        maptile
        |> debug(label: "findcheats #{maxrange} in")
        |> neighboursatmax(maxrange)
        |> List.flatten()
        |> Enum.filter(fn {p,_n} -> map[p] != :wall end) # don't end in a wall
        |> Enum.filter(fn {p,_n} -> map[p] != nil end) # don't end off the map
        |> Enum.map(fn {p, n} -> {maptile, p, map[p] - steps - n} end)
        |> Enum.filter(fn {_p1, _p2, saved} -> saved > 0 end)
        # |> Enum.map(fn cheat -> vizcheat(cheat, map) end)
        |> debug(label: "findcheats #{maxrange} out")
    end

    def counter({_p1, _p2, saved}, accum) do
        Map.put(accum, saved, Map.get(accum, saved, 0) + 1)
    end

    def runpart1(map, cheatdistance, minsaved) do
        map
        |> Enum.filter(fn {p, v} -> (
            p != :start
            and p != :end
            and v != :wall
        )end)
        |> Enum.map(fn tile -> findcheats(tile, map, cheatdistance) end)
        # |> Task.async_stream(fn tile -> {tile, findcheats(tile, map)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        |> debug(label: "run1 0")
        |> List.flatten()
        |> Enum.filter(fn {p1, p2, saved} -> saved >= minsaved end)
        |> then(fn x ->
            info(length(x), label: "run1 length total")
            x
        end)
        |> MapSet.new() # unique
        |> then(fn x ->
            info(MapSet.size(x), label: "run1 length unique")
            x
        end)
        |> debug(label: "run1")

        # |> Enum.reduce(%{}, fn cheat, acc -> counter(cheat, acc) end)
        |> MapSet.size()

        # |> Enum.map(fn line -> {line, todo1(line)} end)
        |> debug(label: "run2")
        # |> Enum.count(fn {_line, sl} -> sl end)
        # |> debug(label: "run3")
    end

end


Puzzleday20.read_input("input/2024/day20inputtest.txt")
|> Puzzleday20.runpart1(2, 0)
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzleday20.read_input("input/2024/day20input.txt")
|> Puzzleday20.runpart1(2, 100)
|> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday20.read_input("input/2024/day20inputtest.txt")
|> Puzzleday20.runpart1(20, 50)
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday20.read_input("input/2024/day20input.txt")
|> Puzzleday20.runpart1(20, 100)
|> IO.inspect(pretty: true, label: "realinput, part2")
