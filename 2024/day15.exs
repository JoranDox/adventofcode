


defmodule Puzzleday15 do
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

    def mapsetbounds(mapset) do
        mapset
        # |> debug(label: "mapsetbounds 0")
        |> Enum.map(fn p -> [p.x, p.y] end)
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
        [maxx, maxy] = bounds(map)
        log_level = System.get_env("LOG_LEVEL")
        if log_level in ["debug", "info"] or force do
            Enum.reduce(0..maxy, "", fn y, _acc ->
                Enum.reduce(0..maxx, "", fn x, acc2 ->
                    case map[%Point2d{x: x,y: y}] do
                        nil -> acc2 <> " "
                        :box -> acc2 <> "O"
                        :wall -> acc2 <> "#"
                        :robot -> acc2 <> "@"

                    end
                end)
                |> info([label: "twodeeviz 1"], force)
            end)
        end
        info("", [label: "twodeeviz 2"], force)
        map
    end

    def testinput do
        read_input("input/2024/day15inputtest.txt")
    end

    def testinput_small do
        read_input("input/2024/day15inputtest_small.txt")
    end

    def realinput do
        read_input("input/2024/day15input.txt")
    end


    def point2dstep(p, :up), do: %Point2d{x: p.x, y: p.y-1}
    def point2dstep(p, :down), do: %Point2d{x: p.x, y: p.y+1}
    def point2dstep(p, :left), do: %Point2d{x: p.x-1, y: p.y}
    def point2dstep(p, :right), do: %Point2d{x: p.x+1, y: p.y}

    def trystep(map, robotorbox, direction) do
        newpos = point2dstep(robotorbox, direction)
        case Map.get(map, newpos) do
            nil -> {true, newpos}
            :wall -> {false, nil}
            :box -> trystep(map, newpos, direction)
            :robot -> {false, nil}
        end
    end

    def read_input(filename) do
        [map, moves] = (
            File.read!(filename)
            |> String.split("\n\n", trim: true)
            |> debug(label: "read_input 1")
        )

        {
            map
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
                                "#" -> {%Point2d{x: x, y: y}, :wall}
                                "O" -> {%Point2d{x: x, y: y}, :box}
                                "@" -> [{%Point2d{x: x, y: y}, :robot}, {:robot, %Point2d{x: x, y: y}}]
                            end
                        end
                    )
                end
            )
            |> List.flatten()
            |> Enum.filter(fn x -> x != nil end)
            |> Map.new()
            |> debug(label: "read_input map", limit: :infinity),
            moves
            |> String.split("", trim: true)
            |> Enum.map(
                fn char ->
                    case char do
                        "^" -> :up
                        "v" -> :down
                        "<" -> :left
                        ">" -> :right
                        _ -> nil
                    end
                end
            )
            |> Enum.filter(fn x -> x != nil end)
            |> debug(label: "read_input moves")
        }


        |> debug(label: "read_input 3")
    end

    def steps([], _robot, map) do
        map
    end
    def steps([move | moves], robot, map) do
        debug({robot, move}, label: "steps")
        twodeeviz(map)
        {canstep, finalpos} = trystep(map, robot, move)
        |> debug(label: "steps trystep")
        debug(map[finalpos], label: "steps finalpos")
        debug(map[robot], label: "steps robot")
        if canstep do
            newpos = point2dstep(robot, move)
            debug(map[newpos], label: "steps newpos")
            # if new position is a box, move the box
            map = if map[newpos] == :box do
                Map.put(map, finalpos, :box)
            else
                map
            end
            # move robot
            map = Map.put(map, robot, nil)
            map = Map.put(map, newpos, :robot)
            debug(map[finalpos], label: "steps finalpos after move")
            debug(map[robot], label: "steps robot after move")
            debug(map[newpos], label: "steps newpos after move")
            steps(moves, newpos, map)
        else
            newpos = robot
            steps(moves, newpos, map)
        end
    end

    def score(map) do
        map
        |> Enum.map(fn {p, type} ->
            if type == :box do
                p.x + 100*p.y
            else
                0
            end
        end)
    end

    def runpart1({map, moves}) do
        {robot, map} = Map.pop(map, :robot)
        steps(moves, robot, map)
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        # |> Enum.map(fn line -> {line, todo1(line)} end)
        |> debug(label: "run2")
        |> score()
        # |> Enum.count(fn {_line, sl} -> sl end)
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


Puzzleday15.testinput()
|> Puzzleday15.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzleday15.realinput()
|> Puzzleday15.runpart1()
|> IO.inspect(pretty: true, label: "realinput, part1")

# Puzzleday15.testinput()
# |> Puzzleday15.runpart2()
# |> IO.inspect(pretty: true, label: "testinput, part2")

# Puzzleday15.realinput()
# |> Puzzleday15.runpart2()
# |> IO.inspect(pretty: true, label: "realinput, part2")
