


defmodule Puzzleday06 do
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

    def twodeeviz({contordont, map}, force\\false) do
        log_level = System.get_env("LOG_LEVEL")
        if log_level in ["debug", "info"] or force do
            Enum.reduce(0..map.maxy, "", fn y, _acc ->
                Enum.reduce(0..map.maxx, "", fn x, acc2 ->
                    case map[{x,y}] do
                        nil -> acc2 <> " "
                        :obstacle -> acc2 <> "#"
                        :up -> acc2 <> "^"
                        :down -> acc2 <> "v"
                        :left -> acc2 <> "<"
                        :right -> acc2 <> ">"
                        _ -> acc2 <> "?"
                    end
                end)
                |> info([label: "twodeeviz 1"], force)
            end)
        end
        info("", [label: "twodeeviz 1"], force)
        {contordont, map}

    end

    def testinput do
        read_input("input/2024/day06inputtest.txt")
    end

    def realinput do
        read_input("input/2024/day06input.txt")
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
                    "#" -> {{xindex, yindex}, :obstacle}
                    "^" -> [{:agent, {{xindex, yindex}, :up}}, {{xindex, yindex}, :up}]
                end
                |> debug(label: "read_input 5")
            end)
        end)
        |> debug(label: "read_input 6")
        |> List.flatten()
        |> debug(label: "read_input 7")
        |> Enum.filter(fn x -> x != nil end)
        |> debug(label: "read_input 8")
        |> Enum.reduce(%{}, fn {key, value}, acc -> Map.put(acc, key, value) end)
        |> debug(label: "read_input 9")
        |> then(fn map ->
            map
            |>Map.put(:maxx, Enum.max(Enum.map(Map.keys(map), fn key ->
                case key do
                    {x,_y} -> x
                    _ -> 0
                end
            end)))
            |>Map.put(:maxy, Enum.max(Enum.map(Map.keys(map), fn key ->
                case key do
                    {_x,y} -> y
                    _ -> 0
                end
            end)))
        end)
        |> debug(label: "read_input 10")
    end

    def turnright(direction) do
        case direction do
            :up -> :right
            :right -> :down
            :down -> :left
            :left -> :up
        end
    end

    def checkstep(map, {oldpos, newpos, direction}) do
        case map[newpos] do
            :obstacle -> {oldpos, turnright(direction), :nopart2}
            ^direction -> {newpos, direction, :loop_detected} # TODO fit this in the existing code
            _ -> {newpos, direction, :nopart2}
        end
    end

    def step({x,y}, direction) do
        case direction do
            :up -> {x, y-1}
            :down -> {x, y+1}
            :left -> {x-1, y}
            :right -> {x+1, y}
        end
    end

    def onestep(map) do
        {loc, direction} = map.agent
        checkstep(map, {loc, step(loc, direction), direction})
        |> debug(label: "onestep 1")

    end

    def outofbounds({{x,y}, _direction}, map) do
        (
            x < 0
            or x > map.maxx
            or y < 0
            or y > map.maxy
        )
    end

    def simonestep(step_n, map) do
        step = onestep(map)
        {loc, direction, extra_info} = step
        step = {loc, direction} # remove extra_info
        map = Map.put(map, :path, [step(loc, direction) | Map.get(map, :path, [])]) # next step is overlap, step after that is where we want to put a blocker
        |> info(label: "simonestep #{step_n} newmap1")

        if step_n > 100000 do
            # info("long path detected", [label: "simonestep #{step_n} 0"], true)
            # twodeeviz({1, map}, true)
            {:halt, Map.put(map, :loop_detected, :loop_detected)}
        else
            if extra_info == :loop_detected do
                debug("loop detected", label: "simonestep #{step_n} 0")
                {:halt, Map.put(map, :loop_detected, :loop_detected)}
            else
                if outofbounds(step, map) do
                    debug("out of bounds", label: "simonestep #{step_n} 1")
                    {:halt, map}
                else
                    debug("still going strong", label: "simonestep #{step_n} 2")
                    {:cont, Map.put(map, :agent, step) |> Map.put(loc, direction)}
                end
            end
        end
        |> debug(label: "simonestep #{step_n} 3")
        |> twodeeviz()

    end

    def common(input) do
        input
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        |> debug(label: "run1")
        |> then(fn map -> Enum.reduce_while(1..100000000, map, &simonestep/2) end)
        |> debug(label: "run2", limit: :infinity)
    end

    def runpart1(input) do
        input
        |> common()
        |> Map.values()
        |> debug(label: "run1 3")
        |> Enum.filter(fn key -> key in [:up, :down, :left, :right] end)
        |> debug(label: "run1 4")
        |> Enum.count()
        |> debug(label: "run1 5")
    end

    def runpart2(input) do
        input
        |> common()
        |> info(label: "run2 1")
        |> then(fn map ->
            info(length(map.path), label: "map path len")
            map
        end)
        |> then(fn map ->
            map.path
            |> MapSet.new()
            |> Enum.filter(fn loc -> elem(map.agent, 0) != loc end)
            # List.flatten(
            # Enum.map(0..map.maxy, fn y ->
            #     Enum.map(0..map.maxx, fn x ->
            #         {x,y}
            #     end)
            # end))
            |> Task.async_stream(
            # |> Enum.map(
                fn loc ->
                    # info(loc, [label: "run2 2"], true)
                    input
                    |> Map.put(loc, :obstacle)
                    |> common()
                    |> then(fn map ->
                        if map[:loop_detected] == :loop_detected do
                            # twodeeviz({1, map}, true)
                            1
                        else
                            0
                        end
                    end)
                    |> debug(label: "run2 3")
                end,
                timeout: :infinity
                # end
            )
            |> Enum.map(fn {:ok, result} -> result end)
            |> Enum.sum()
            |> debug(label: "run2 4")
        end)
    end
end

Puzzleday06.testinput()
|> Puzzleday06.common
|> Puzzleday06.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")

# Puzzleday06.realinput()
# |> Puzzleday06.runpart1()
# |> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday06.testinput()
|> Puzzleday06.runpart2()
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday06.realinput()
|> Puzzleday06.runpart2()
|> IO.inspect(pretty: true, label: "realinput, part2")
# 1685 too low
# 1686 also too low
