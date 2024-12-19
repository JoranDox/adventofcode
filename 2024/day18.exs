


defmodule Puzzleday18 do
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

    def twodeeviz(map, {maxx, maxy}, force\\false) do
        log_level = System.get_env("LOG_LEVEL")
        if log_level in ["debug", "info"] or force do
            Enum.reduce(0..maxy, "", fn y, _acc ->
                Enum.reduce(0..maxx, "", fn x, acc2 ->
                    case map[{ x, y}] do
                        nil -> acc2 <> " "
                        :wall -> acc2 <> "#"
                        :start -> acc2 <> "S"
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
        |> debug(label: "read_input 1")
        |> Enum.map(
            fn line ->
                line
                |> String.split(",")
                |> Enum.map(&String.to_integer/1)
            end
        )
        |> debug(label: "read_input 2")
        |> debug(label: "read_input 3")
    end

    def maxes(inlist) do
        inlist
        |> Enum.reduce({0, 0}, fn [x, y], {maxx, maxy} ->
            {max(maxx, x), max(maxy, y)}
        end)
    end

    def shortestpath(map, goal, heapqueue, bestseen) do
        debug(map, label: "shortestpath in map")
        debug(goal, label: "shortestpath in goal")
        # debug(heapqueue, label: "shortestpath in heapqueue")
        debug(bestseen, label: "shortestpath in bestseen")
        {{cost, position}, path, heapqueue} = :gb_trees.take_smallest(heapqueue)
        debug(cost, label: "shortestpath in cost")
        debug(position, label: "shortestpath in position")
        debug(path, label: "shortestpath in path")
        {maxx, maxy} = goal
        # twodeeviz(Map.put(map, position, :start), maxx, maxy)
        case position do
            ^goal -> {cost, path}
            {x,y} -> (
                potentials = (
                    [
                        {x+1, y},
                        {x-1, y},
                        {x, y+1},
                        {x, y-1}
                    ]
                    |> Enum.filter(fn {x, y} -> x >= 0 and y >= 0 end)
                    |> Enum.filter(fn {x, y} -> x <= maxx and y <= maxy end)
                    |> Enum.filter(fn {x, y} -> map[{x, y}] != :wall end)
                    |> Enum.filter(fn {x, y} ->
                        case bestseen[{x, y}] do
                            nil -> true
                            seencost -> seencost > cost
                        end
                    end)
                    # |> Enum.map(fn {x, y} -> {cost+1, {x, y}} end)
                )
                |> debug(label: "shortestpath potentials")
                shortestpath(
                    map,
                    goal,
                    potentials
                    |> Enum.reduce(heapqueue, fn pos, acc ->
                        :gb_trees.enter( {cost+1, pos}, [pos | path] |> debug(label: "putting path"), acc )
                    end),
                    potentials
                    |> Enum.reduce(bestseen, fn pos, acc ->
                        Map.put(acc, pos, cost+1)
                    end)
                )
            )
        end
    end

    def runpart1(input, n) do
        {maxx, maxy} = maxes(input) |> debug(label: "maxes")


        |> debug(label: "run2")

        startpos = {0, 0}
        goal = {maxx, maxy}

        map = (
            input
            |> Enum.take(n)
            |> Enum.map(fn [x, y] -> {{x, y}, :wall} end)
            |> Map.new()
        )
        # twodeeviz(map, goal)
        heapqueue = :gb_trees.empty()
        heapqueue = :gb_trees.enter( {0, startpos}, [startpos], heapqueue )

        {
            shortestpath(map, goal, heapqueue, Map.put(%{}, startpos, 0))
            |> debug(label: "run3"),
            map
        }

    end

    def dropwhile([], _) do
        []
    end
    def dropwhile([head | tail], pred) do
        case pred.(head) do
            true -> dropwhile(tail, pred)
            false -> [head | tail]
        end
    end

    def runpart2(input) do
        goal = maxes(input)
        input
        |> Enum.with_index()
        # |> dropwhile(fn x -> x != [40, 14] end)
        |> Enum.map(fn {block, i} ->
            info({block, i}, label: "runpart2 block")
            {{cost, path}, map} = runpart1(input, i)
            path
            |> Enum.map(fn loc ->{loc, :path} end)
            |> Map.new()
            |> Map.merge(map)
            |> twodeeviz(goal)

        end)
        # |> Enum.map(fn line -> {line, todo2(line)} end)
        |> debug(label: "run2")
        # |> Enum.count(fn {_line, sl} -> sl end)
        |> debug(label: "run3")
    end
end


Puzzleday18.read_input("input/2024/day18inputtest.txt")
|> Puzzleday18.runpart1(12)
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzleday18.read_input("input/2024/day18input.txt")
|> Puzzleday18.runpart1(1024)
|> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday18.read_input("input/2024/day18inputtest.txt")
|> Puzzleday18.runpart2()
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday18.read_input("input/2024/day18input.txt")
|> Puzzleday18.runpart2()
|> IO.inspect(pretty: true, label: "realinput, part2")
