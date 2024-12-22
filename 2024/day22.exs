


defmodule Puzzleday22 do
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

    def mix(secret, value) do
        Bitwise.bxor(secret, value)
    end

    def prune(secret) do
        Integer.mod(secret, 16777216)
    end


    def iterate(secret) do
        value = secret * 64
        secret = mix(secret, value)
        secret = prune(secret)
        # value = round(secret / 32)
        value = div(secret, 32)
        # debug({div(secret, 32), value, secret / 32, round(secret / 32)}, label: "iterate after div")
        secret = mix(secret, value)
        secret = prune(secret)
        value = secret * 2048
        secret = mix(secret, value)
        secret = prune(secret)
        secret
    end

    def read_input(filename) do
        File.read!(filename)
        |> String.split("\n", trim: true)
        |> debug(label: "read_input 1")
        |> debug(label: "read_input 2")
        |> Enum.map(
            fn line -> String.to_integer(line) end
        )
        |> debug(label: "read_input 3")
    end

    def runpart1(input) do
        input
        |> Task.async_stream(fn num ->
        # |> Enum.map(fn num ->
            1..2000
            |> Enum.reduce(num, fn _, secret -> iterate(secret) end)
            |> debug(label: "run1 #{num}")
        end)
        |> Enum.map(fn {:ok, result} -> result end)
        |> debug(label: "run2")
        |> Enum.sum()
        |> debug(label: "run3")
        # |> Enum.map
        # |> Enum.map(fn line -> {line, todo1(line)} end)
        # |> debug(label: "run2")
        # |> Enum.count(fn {_line, sl} -> sl end)
        # |> debug(label: "run3")
    end

    def prices(list) do
        list
        |> Enum.map(fn num ->
            # {num, Integer.mod(num, 10)}
            Integer.mod(num, 10)
        end)
    end


    def changes([first]) do
        [{first, nil}]
    end
    def changes([last, nexttolast | tail]) do
        # running difs over the list, note the list is still reversed
        [{last, last - nexttolast} | changes([nexttolast | tail])]
    end

    def possiblesequencesandtheirprices(list) do
        Enum.zip([
            list,
            list |> tl(),
            list |> tl() |> tl(),
            list |> tl() |> tl() |> tl()
        ])
        |> Enum.reduce(%{}, fn {{ap,ad},{bp,bd},{cp,cd},{dp,dd}}, seen ->
            sequence = {ad,bd,cd,dd}
            price = dp
            if sequence not in Map.keys(seen) do
                Map.put(seen, sequence, price)
            else
                seen
            end
            # case result do
            #     {{-2,1,-1,3}, price} -> debug({price}, label: "price seen for -2,1,-1,3")
            #     {{-2, 2, -1, -1}, price} -> debug({price}, label: "price seen for -2,2,-1,-1")
            #     _ -> nil
            # end
            # result
        end)
    end

    def runpart2(input) do
        input
        |> Task.async_stream(fn num ->
        # |> Enum.map(fn num ->
            1..2000
            |> Enum.reduce(
                [num],
                fn _, [lastsecret | tail] ->
                    [iterate(lastsecret), lastsecret | tail] end)
            |> debug(label: "run1 #{num}")
        end)
        |> Enum.map(fn {:ok, result} -> result end)
        |> debug(label: "run2")
        |> Enum.map(fn secrets -> prices(secrets) end)
        |> debug(label: "run3")
        |> Enum.map(fn prices -> changes(prices) end)
        |> debug(label: "run4")
        |> Enum.map(fn changes -> Enum.reverse(changes) |> tl() end)
        |> debug(label: "run5")
        |> Enum.map(fn changes -> possiblesequencesandtheirprices(changes) end)
        |> debug(label: "run6")
        |> Enum.reduce(%{}, fn newseen, seen ->
            Map.merge(newseen, seen, fn _key, newval, oldval -> newval + oldval end)
        end)
        # |> List.flatten()
        |> debug(label: "run7")
        # |> Enum.reduce(%{}, fn {difs, price}, acc ->
        #     Map.put(acc, difs, Map.get(acc, difs, 0) + price)
        # end)
        |> debug(label: "run8")
        |> then(fn bigmap ->
            debug(bigmap[{-2,1,-1,3}], label: "run8 -2,1,-1,3")
            bigmap
        end)
        |> Enum.max_by(fn {difs, price} -> price end)
        |> debug(label: "run9")

    end
end



42
|> Puzzleday22.mix(15)
|> Puzzleday22.debug(label: "mix")

100000000
|> Puzzleday22.prune()
|> Puzzleday22.debug(label: "prune")

123
|> Puzzleday22.iterate()
|> Puzzleday22.debug(label: "iterate")
|> Puzzleday22.iterate()
|> Puzzleday22.debug(label: "iterate")
|> Puzzleday22.iterate()
|> Puzzleday22.debug(label: "iterate")
|> Puzzleday22.iterate()
|> Puzzleday22.debug(label: "iterate")
|> Puzzleday22.iterate()
|> Puzzleday22.debug(label: "iterate")
|> Puzzleday22.iterate()
|> Puzzleday22.debug(label: "iterate")
|> Puzzleday22.iterate()
|> Puzzleday22.debug(label: "iterate")

Puzzleday22.read_input("input/2024/day22inputtest.txt")
|> Puzzleday22.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzleday22.read_input("input/2024/day22input.txt")
|> Puzzleday22.runpart1()
|> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday22.read_input("input/2024/day22inputtest.txt")
|> Puzzleday22.runpart2()
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday22.read_input("input/2024/day22input.txt")
|> Puzzleday22.runpart2()
|> IO.inspect(pretty: true, label: "realinput, part2")
