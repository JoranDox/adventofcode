require Integer


defmodule Puzzleday11 do
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
        read_input("input/2024/day11inputtest.txt")
    end

    def realinput do
        read_input("input/2024/day11input.txt")
    end

    def blink(stone) do
        if stone == 0 do
            [1]
        else
            debug(stone, label: "blink in")
            String.length(Integer.to_string(stone)) |> debug(label: "len(x)")
            stonestr = Integer.to_string(stone)
            case String.length(stonestr) do
                len when Integer.is_even(len) -> [
                    String.to_integer(String.slice(stonestr, 0, div(len,2))),
                    String.to_integer(String.slice(stonestr, -div(len,2), div(len,2)))
                ]
                _ -> [(stone * 2024)]
            end
            |> debug(label: "blink out")
        end
    end

    def cache_stone(map, stone, 1) do
        debug(stone, label: "cache_stone 1 in")
        if Map.has_key?(map, {stone, 1}) do
            debug(stone, label: "cache_stone 1 cache hit")
            map
        else
            debug(stone, label: "cache_stone 1 cache miss")
            Map.put(
                map,
                {stone, 1},
                blink(stone)
                |> debug(label: "cache_stone 1 after blink")
            )
        end
        |> debug(label: "cache_stone 1 out")
    end
    def cache_stone(map, stone, n) do
        debug(stone, label: "cache_stone #{n} in")
        if Map.has_key?(map, {stone, n}) do
            debug(stone, label: "cache_stone #{n} cache hit")
            map
        else
            debug(stone, label: "cache_stone #{n} cache miss")
            newmap = cache_stone(map, stone, n-1)
            Map.put(
                newmap,
                {stone, n},
                Map.get(newmap, {stone, n-1})
                |> debug(label: "cache_stone #{n} before blink")
                |> Enum.map(fn stone -> stone |> blink() end)
                |> debug(label: "cache_stone #{n} after blink")
                |> List.flatten()
            )
        end
        |> debug(label: "cache_stone #{n} out")
    end


    def cache_stone_2(map, stone, 1) do
        debug(stone, label: "cache_stone 1 in")
        if Map.has_key?(map, {stone, 1}) do
            debug(stone, label: "cache_stone 1 cache hit")
            map
        else
            debug(stone, label: "cache_stone 1 cache miss")
            map = Map.put(
                map,
                {:result, stone, 1},
                blink(stone)
                |> debug(label: "cache_stone 1 after blink")
                |> List.flatten()
            )
            Map.put(
                map,
                {:length, stone, 1},
                Map.get(map, {:result, stone, 1})
                |> Enum.count()
                |> debug(label: "cache_stone 1 count")
            )
        end
        |> debug(label: "cache_stone 1 out")
    end
    def cache_stone_2(map, stone, n) do
        debug(stone, label: "cache_stone #{n} in")
        if Map.has_key?(map, {stone, n}) do
            debug(stone, label: "cache_stone #{n} cache hit")
            map
        else
            debug(stone, label: "cache_stone #{n} cache miss")
            blinked = cache_stone_2(map, stone, 1) |> Map.get({:result, stone, 1})
            map = Enum.reduce(blinked, map, fn newstone, acc ->
                cache_stone_2(acc, newstone, n-1)
            end)
            Map.put(
                map,
                {:length, stone, n},
                blinked
                |> Enum.map(fn newstone ->
                    Map.get(map, {:length, newstone, n-1})
                end)
                |> debug(label: "cache_stone #{n} before sum")
                |> Enum.sum()
                |> debug(label: "cache_stone #{n} after sum")
            )
        end
        |> debug(label: "cache_stone #{n} out")
    end

    def read_input(filename) do
        File.read!(filename)
        # |> String.split("\n", trim: true)
        |> debug(label: "read_input 1")
        |> String.split(" ", trim: true)
        |> debug(label: "read_input 2")
        |> Enum.map(
            fn stone -> String.to_integer(stone) end
        )
        |> debug(label: "read_input 3")
    end

    def runpart1(stones, num) do
        cache = (
            stones
            |> Enum.reduce(%{}, fn stone, acc ->
                cache_stone(acc, stone, num)
            end)
            |> debug(label: "merged map")
        )

        stones
        |> Enum.map(fn stone ->
            Map.get(cache, {stone, num})
        end)
        |> debug(label: "run1")
        |> List.flatten()
        |> debug(label: "run2")
        |> Enum.count()
        |> debug(label: "run3")
        # |> Enum.map(fn stone ->
        #     map = cache_stone(%{}, stone, 25)
        #     map
        #     |> debug(label: "run1 #{stone} #{Map.get(map,stone)}")
        # end)
        # |> debug(label: "run1")
        # |> List.flatten()
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        # |> Enum.map(fn line -> {line, todo1(line)} end)
    end

    def runpart2(stones, num) do
        cache = (
            stones
            |> Enum.reduce(%{}, fn stone, acc ->
                cache_stone_2(acc, stone, num)
            end)
            |> info(label: "merged map")
        )

        stones
        |> Enum.map(fn stone ->
            debug(stone, label: "stone1")
            Map.get(cache, {:length, stone, num})
        end)
        |> debug(label: "run1")
        |> List.flatten()
        |> debug(label: "run2")
        |> Enum.sum()
        |> debug(label: "run3")
    end
end

Puzzleday11.testinput()
|> Puzzleday11.runpart1(25)
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzleday11.realinput()
|> Puzzleday11.runpart1(25)
|> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday11.testinput()
|> Puzzleday11.runpart2(25)
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday11.realinput()
|> Puzzleday11.runpart2(25)
|> IO.inspect(pretty: true, label: "realinput, part2")

Puzzleday11.realinput()
|> Puzzleday11.runpart2(75)
|> IO.inspect(pretty: true, label: "realinput, part2, 75")
