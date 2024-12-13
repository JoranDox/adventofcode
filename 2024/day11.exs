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
        debug(stone, label: "cache_stone_2 1 in")
        if Map.has_key?(map, {:results, stone, 1}) do
            debug(stone, label: "cache_stone_2 1 cache hit")
            map
        else
            debug(stone, label: "cache_stone_2 1 cache miss")
            map = Map.put(
                map,
                {:result, stone, 1},
                blink(stone)
                |> debug(label: "cache_stone_2 1 after blink")
                |> List.flatten()
            )
            Map.put(
                map,
                {:length, stone, 1},
                Map.get(map, {:result, stone, 1})
                |> Enum.count()
                |> debug(label: "cache_stone_2 1 count")
            )
        end
        |> debug(label: "cache_stone_2 1 out")
    end
    def cache_stone_2(map, stone, n) do
        debug(stone, label: "cache_stone_2 n=#{n} in")
        if Map.has_key?(map, {:result, stone, n}) do
            debug(stone, label: "cache_stone_2 n=#{n} cache hit")
            map
        else
            debug(stone, label: "cache_stone_2 n=#{n} cache miss")
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
                |> debug(label: "cache_stone_2 n=#{n} before sum")
                |> Enum.sum()
                |> debug(label: "cache_stone_2 n=#{n} after sum")
            )
        end
        |> debug(label: "cache_stone_2 n=#{n} out")
    end

    def etshaskey?(key) do
        :ets.lookup(:cache, key) != []
    end
    def etsput(key, value) do
        :ets.insert(:cache, {key, value})
    end
    def etsget(key) do
        :ets.lookup(:cache, key)
        |> hd()
        |> elem(1)
    end

    def cache_stone_ets(stone, 1) do
        debug(stone, label: "cache_stone_ets 1 in")
        if etshaskey?({:result, stone, 1}) do
            debug(stone, label: "cache_stone_ets 1 cache hit")
            true
        else
            debug(stone, label: "cache_stone_ets 1 cache miss")
            blinked = (
                blink(stone)
                |> debug(label: "cache_stone_ets 1 after blink")
                |> List.flatten()
            )

            etsput(
                {:result, stone, 1},
                blinked
            )
            etsput(
                {:length, stone, 1},
                blinked
                |> Enum.count()
                |> debug(label: "cache_stone_ets 1 count")
            )
            false
        end
        |> debug(label: "cache_stone_ets 1 out")
    end
    def cache_stone_ets(stone, n) do
        debug(stone, label: "cache_stone_ets n=#{n} in")
        if etshaskey?({:result, stone, n}) do
            if n == 25 do
                debug(stone, label: "cache_stone_ets cache hit n=#{n}")
            else
                debug(stone, label: "cache_stone_ets cache hit n=#{n}")
            end
            true
        else
            debug(stone, label: "cache_stone_ets cache miss n=#{n}")
            cache_stone_ets(stone, 1) # ensure this is cached
            blinked = etsget({:result, stone, 1})
            blinked
            # |> Task.async_stream(fn newstone -> cache_stone_ets(newstone, n-1) end, timeout: :infinity)
            # |> Enum.map(fn {:ok, result} -> result end)
            |> Enum.map(fn newstone -> cache_stone_ets(newstone, n-1) end)

            etsput(
                {:length, stone, n},
                blinked
                |> Enum.map(fn newstone ->
                    etsget({:length, newstone, n-1})
                end)
                |> debug(label: "cache_stone_2 n=#{n} before sum")
                |> Enum.sum()
                |> debug(label: "cache_stone_2 n=#{n} after sum")
            )
            false
        end
        |> debug(label: "cache_stone_2 n=#{n} out")
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
                debug(stone, label: "stone input")
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

    def runpart2(stones, total) do
        cache = %{}
        1..total
        |> Enum.map(fn num ->
            cache = (
                stones
                |> Enum.reduce(cache, fn stone, acc ->
                    cache_stone_2(acc, stone, num)
                end)
                |> debug(label: "merged map #{num}")
            )

            cache
            |> map_size()
            |> debug(label: "merged map size #{num}")

            stones
            |> Enum.map(fn stone ->
                debug(stone, label: "stone1 #{num}")
                Map.get(cache, {:length, stone, num})
            end)
            |> debug(label: "run1 #{num}")
            |> List.flatten()
            |> debug(label: "run2 #{num}")
            |> Enum.sum()
            |> debug(label: "run3 #{num}")
        end)
    end

    def runpart2_ets(stones, total) do
        1..total
        |> Task.async_stream(fn num ->
            # ensure cached
            stones
            |> Task.async_stream(fn stone -> cache_stone_ets(stone, num) end, timeout: :infinity)
            |> Enum.map(fn {:ok, result} -> result end)
            # |> Enum.map(fn stone -> cache_stone_ets(stone, num) end)
            # cache
            # |> map_size()
            # |> info(label: "merged map size #{num}")

            stones
            |> Enum.map(fn stone ->
                debug(stone, label: "stone1 #{num}")
                etsget({:length, stone, num})
            end)
            |> debug(label: "run1 #{num}")
            |> List.flatten()
            |> debug(label: "run2 #{num}")
            |> Enum.sum()
            |> debug(label: "run3 #{num}")
        end,
        timeout: :infinity)
        |> Enum.map(fn {:ok, result} -> result end)

        stones
        |> Enum.map(fn stone ->
            etsget({:length, stone, total})
        end)
        |> Enum.sum()
    end

    def stonelisttomap(stones) do
        Enum.reduce(stones, %{}, fn {stone, num}, acc ->
            Map.put(acc, stone, num + Map.get(acc, stone, 0))
        end)
    end

    def runattempt3(stones, total) do
        # ensure cached
        counter = (
            stones
            |> Enum.map(fn stone -> {stone, 1} end)
            |> stonelisttomap()
            |> debug(label: "run3 starting stone counter")
        )

        1..total
        |> Enum.reduce(counter, fn iteration, stones ->
            stones
            |> debug(label: "run3 iteration #{iteration}")
            |> Enum.map(fn {stone, count} ->
                blink(stone)
                |> debug(label: "run3 blinked #{stone}")
                |> Enum.map(fn newstone -> {newstone, count} end)
            end)
            |> debug(label: "run3 blinked")
            |> List.flatten()
            |> debug(label: "run3 flattened")
            |> stonelisttomap()
            |> debug(label: "run3 stonelisttomap")

        end)
        |> debug(label: "run3 result")
        |> Enum.map(fn {_stone, count} -> count end)
        |> Enum.sum()
        |> debug(label: "run3 sum")
        # |> Task.async_stream(fn stone -> cache_stone_ets(stone, num) end, timeout: :infinity)
        # |> Enum.map(fn {:ok, result} -> result end)
        # # |> Enum.map(fn stone -> cache_stone_ets(stone, num) end)
        # # cache
        # # |> map_size()
        # # |> info(label: "merged map size #{num}")

        # stones
        # |> Enum.map(fn stone ->
        #     debug(stone, label: "stone1 #{num}")
        #     etsget({:length, stone, num})
        # end)
        # |> info(label: "run1 #{num}")
        # |> List.flatten()
        # |> info(label: "run2 #{num}")
        # |> Enum.sum()
        # |> info(label: "run3 #{num}")

        # stones
        # |> Enum.map(fn stone ->
        #     etsget({:length, stone, total})
        # end)
        # |> Enum.sum()
    end

end

:ets.new(:cache, [:public, :named_table])

# Puzzleday11.testinput()
# |> Puzzleday11.runpart1(25)
# |> IO.inspect(pretty: true, label: "testinput, part1")

# Puzzleday11.realinput()
# |> Puzzleday11.runpart1(25)
# |> IO.inspect(pretty: true, label: "realinput, part1")

# Puzzleday11.testinput()
# |> Puzzleday11.runpart2(3)
# |> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday11.testinput()
|> Puzzleday11.runpart2_ets(4)
|> IO.inspect(pretty: true, label: "testinput, 4")

# Puzzleday11.testinput()
# |> Puzzleday11.runpart2_ets(25)
# |> IO.inspect(pretty: true, label: "testinput, 25")

# Puzzleday11.realinput()
# |> Puzzleday11.runpart2_ets(25)
# |> IO.inspect(pretty: true, label: "realinput, part2")

# Puzzleday11.realinput()
# |> Puzzleday11.runpart2_ets(75)
# |> IO.inspect(pretty: true, label: "realinput, part2, 75")

Puzzleday11.testinput()
|> Puzzleday11.runattempt3(4)
|> IO.inspect(pretty: true, label: "testinput, 4")

Puzzleday11.testinput()
|> Puzzleday11.runattempt3(25)
|> IO.inspect(pretty: true, label: "testinput, 25")

Puzzleday11.realinput()
|> Puzzleday11.runattempt3(25)
|> IO.inspect(pretty: true, label: "realinput, part2")

Puzzleday11.realinput()
|> Puzzleday11.runattempt3(75)
|> IO.inspect(pretty: true, label: "realinput, part2, 75")
