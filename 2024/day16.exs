


defmodule Puzzleday16 do
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
        # |> debug(label: "mapsetbounds 0")
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
        # |> debug(label: "bounds 1")
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
                        :path -> acc2 <> "O"
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
                            # "#" -> {%Point2d{x: x, y: y}, :wall}
                            # "S" -> [{%Point2d{x: x, y: y}, :start}, {:start, %Point2d{x: x, y: y}}]
                            # "E" -> {%Point2d{x: x, y: y}, :end}
                            "#" -> {{x, y}, :wall}
                            "S" -> [{{x, y}, :start}, {:start, {x, y}}]
                            "E" -> {{x, y}, :end}
                        end
                    end
                )
            end
        )
        |> List.flatten()
        |> Enum.filter(fn x -> x != nil end)
        |> Map.new()
        # |> debug(label: "read_input map", limit: :infinity)
    end

    def turncw( %Point2d{x:  0, y:  1}) do %Point2d{x: -1, y:  0} end
    def turncw( %Point2d{x: -1, y:  0}) do %Point2d{x:  0, y: -1} end
    def turncw( %Point2d{x:  0, y: -1}) do %Point2d{x:  1, y:  0} end
    def turncw( %Point2d{x:  1, y:  0}) do %Point2d{x:  0, y:  1} end
    def turncw( { 0,  1}) do {-1,  0} end
    def turncw( {-1,  0}) do { 0, -1} end
    def turncw( { 0, -1}) do { 1,  0} end
    def turncw( { 1,  0}) do { 0,  1} end
    def turncw(:up) do :right end
    def turncw(:right) do :down end
    def turncw(:down) do :left end
    def turncw(:left) do :up end
    def turncw(:^) do :> end
    def turncw(:>) do :v end
    def turncw(:v) do :< end
    def turncw(:<) do :^ end
    def turnccw(%Point2d{x:  0, y:  1}) do %Point2d{x:  1, y:  0} end
    def turnccw(%Point2d{x:  1, y:  0}) do %Point2d{x:  0, y: -1} end
    def turnccw(%Point2d{x:  0, y: -1}) do %Point2d{x: -1, y:  0} end
    def turnccw(%Point2d{x: -1, y:  0}) do %Point2d{x:  0, y:  1} end
    def turnccw({ 0,  1}) do { 1,  0} end
    def turnccw({ 1,  0}) do { 0, -1} end
    def turnccw({ 0, -1}) do {-1,  0} end
    def turnccw({-1,  0}) do { 0,  1} end
    def turnccw(:up) do :left end
    def turnccw(:left) do :down end
    def turnccw(:down) do :right end
    def turnccw(:right) do :up end
    def turnccw(:^) do :< end
    def turnccw(:<) do :v end
    def turnccw(:v) do :> end
    def turnccw(:>) do :^ end

    def ptup({x,y}) do
        Tuple.to_list({x,y})
        |> Enum.join(",")
    end

    def moveline(pos, direction, map, stepstohere \\ 1) do
        newloc = point2dsum(pos, direction)
        case map[newloc] do
            nil -> [{stepstohere+1, {newloc, direction}} | moveline(newloc, direction, map, stepstohere+1)]
            :wall -> [:blocked]
            :start -> [:blocked] # there's no way this is efficient
            :end -> [{stepstohere+1, {newloc, direction, :end}}]
        end
    end

    def getpossiblemoves(pos, direction, map, costtohere) do
        List.flatten([
            # moveline(pos, direction, map, costtohere),
            moveline(pos, turncw(direction), map, costtohere+1000),
            moveline(pos, turnccw(direction), map, costtohere+1000)
        ])
        # |> debug(label: "getpossiblemoves #{pos.x},#{pos.y} #{direction.x},#{direction.y}")
        |> debug(label: "getpossiblemoves #{ptup(pos)} #{direction}")
    end

    def expandpath({{x1, y1}, _startdir}, {{x2, y2}, _stopdir}) do
        if x1 == x2 do
            y2..y1 |> Enum.map(fn y -> {x1, y} end)
        else
            x2..x1 |> Enum.map(fn x -> {x, y1} end)
        end
    end

    def expandpathpoint({startpos, _startdir}, {stoppos, stopdir}) do
        # debug({startpos, stoppos, stopdir}, label: "expandpath in")
        if startpos.x == stoppos.x do
            stoppos.y..startpos.y
            |> Enum.map(fn y -> {%Point2d{x: startpos.x, y: y}, stopdir} end)
        else
            stoppos.x..startpos.x
            |> Enum.map(fn x -> {%Point2d{x: x, y: startpos.y}, stopdir} end)
        end
        # |> debug(label: "expandpath out")
    end


    def pqp(heapqueue, map) do
        if :gb_trees.is_empty(heapqueue) do
            heapqueue
        else
            {prio, _value, heapqueue2} = :gb_trees.take_smallest(heapqueue)
            info(prio, label: "pq prio    ")
            # vizpath(value, map)
            pqp(heapqueue2, map)
            heapqueue
        end
    end
    def pqi(heapqueue) do
        if :gb_trees.is_empty(heapqueue) do
            heapqueue
        else
            {prio, _value, heapqueue2} = :gb_trees.take_smallest(heapqueue)
            info(prio, label: "pq prio    ")
            # info(value, label: "pq value        ") # path, ignore now
            pqi(heapqueue2)
            heapqueue
        end
    end

    def vizpath(path, map) do
        Enum.reduce(path, map, fn pos, acc ->
            Map.put(acc, pos, :path)
        end)
        |> twodeeviz()
        path
    end

    def shortestpath({heapqueue, seen}, map, best \\ :infinity, paths \\ []) do
        {{cost, something, path}, _also_path, heapqueue} = :gb_trees.take_smallest(heapqueue)
        debug(cost, label: "something")
        debug(best, label: "shortestpath best")
        if cost > best do
            # we passed the mark of the best path, so we can stop
            {
                best,
                paths
                |> info(label: "all paths")
                # |> Enum.map(fn path -> vizpath(path, map) end)
                |> info(label: "shortestpath paths")
                |> List.flatten()
                # |> Enum.map(fn {{x,y}, _dir} -> {x,y} end)
                |> Enum.reduce(MapSet.new(), fn pathset, acc -> MapSet.union(pathset, acc) end)
                |> info(label: "shortestpath set")
                |> Enum.count()
                |> info(label: "shortestpath end"),
                seen
            }
        else
            case something do
                :end when best == :infinity -> (
                    info(path, label: "shortestpath first end")
                    # info(heapqueue, label: "heapqueue")
                    # pqp(heapqueue, map)
                    shortestpath({heapqueue, seen}, map, cost, [path | paths])
                )
                :end when best == cost -> (
                    info(path, label: "shortestpath extra end")
                    shortestpath({heapqueue, seen}, map, best, [path | paths])
                )
                {pos, direction} -> (
                    getpossiblemoves(pos, direction, map, cost)
                    |> Enum.filter(fn x -> x != :blocked end)
                    |> debug(label: "getpossiblemoves c#{cost} #{ptup(pos)} #{direction}")
                    |> Enum.reduce({heapqueue, seen}, fn({priority, element}, {heapqueue, seen}) ->
                        if (element in path) do
                            debug({something, path}, label: "already been")
                            {heapqueue, seen}
                        else
                            bestseen = seen[element]
                            if bestseen == nil or bestseen >= priority do
                                {newpath, elem} = (
                                    case element do
                                        {pos, dir, :end} -> (
                                            debug({priority, element}, label: "reducing")
                                            {MapSet.union(MapSet.new(expandpath(something, {pos, dir})), path), :end}
                                        )
                                        {_pos, _dir} -> {MapSet.union(MapSet.new(expandpath(something, element)), path), element}
                                    end
                                )
                                newheapqueue = :gb_trees.enter( {priority, elem, newpath}, newpath, heapqueue )
                                # vizpath(newpath, map)
                                {
                                    newheapqueue,
                                    Map.put(seen, elem, priority)
                                }
                            else
                                # if bestseen is nil or bestseen < priority
                                debug({something, path}, label: "already seen better")
                                {heapqueue, seen}
                            end
                        end
                    end)
                    |> debug(label: "before next iter shortestpath")
                    |> shortestpath(map, best, paths)
                )
            end
        end
    end

    def common(input) do
        {startpos, map} = Map.pop(input, :start)
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        # |> Enum.map(fn line -> {line, todo1(line)} end)
        map
        |> twodeeviz()
        startpos
        |> debug(label: "startpos")

        # startdir = %Point2d{x: 1, y: 0}
        # startdir = {1, 0}
        # startdir = :>

        # getpossiblemoves(startpos, startdir, map, 0)
        # # |> Enum.count(fn {_line, sl} -> sl end)
        # |> debug(label: "run3")

        heapqueue = :gb_trees.empty()
        heapqueue = :gb_trees.enter( {0, {startpos, :>}, MapSet.new([startpos])}, MapSet.new([startpos]), heapqueue )
        # cheating to let it start without turning, by inverse turning to begin
        heapqueue = :gb_trees.enter( {-1000, {startpos, :v}, MapSet.new()}, MapSet.new(), heapqueue )
        seen = Map.new([{{startpos, :>}, 0}, {{startpos, :v}, -1000}])
        # seen = Map.new()
        shortestpath({heapqueue, seen}, map)
    end

    def runpart1(input) do
        {cost, _paths, _seen} = common(input)
        |> debug(label: "run1")
        cost
    end

    def runpart2(input) do
        {_cost, _paths, _seen} = common(input)
        |> debug(label: "run2")
    end
end


Puzzleday16.read_input("input/2024/day16inputtest.txt")
|> Puzzleday16.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")

# Puzzleday16.read_input("input/2024/day16input.txt")
# |> Puzzleday16.runpart1()
# |> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday16.read_input("input/2024/day16inputtest.txt")
|> Puzzleday16.runpart2()
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday16.read_input("input/2024/day16input.txt")
|> Puzzleday16.runpart2()
|> IO.inspect(pretty: true, label: "realinput, part2")
