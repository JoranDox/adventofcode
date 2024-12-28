


defmodule Puzzleday19 do
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

    def read_input(filename) do
        [towels, designs] = (
            File.read!(filename)
            |> String.split("\n\n", trim: true)
        )

        towels = (
            towels
            |> String.split(", ", trim: true)
        )

        designs = (
            designs
            |> String.split("\n", trim: true)
        )

        {towels, designs}
        |> debug(label: "read_input 1")
    end

    def runpart1(input) do
        {towels, designs} = input

        {:ok, regex} = (
            ("^(" <> Enum.join(towels, "|") <> ")+$")
            |> debug(label: "regex1")
            |> Regex.compile()
            |> debug(label: "regex2")
        )
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        # |> Enum.map(fn line -> {line, todo1(line)} end)
        # |> debug(label: "run2")
        # # |> Enum.count(fn {_line, sl} -> sl end)
        # |> debug(label: "run3")
        designs
        |> Enum.filter(fn design ->
            Regex.match?(regex, design)
            |> debug(label: "match")
        end)
        |> Enum.count()
    end

    def prefixregexes(towels) do
        towels
        |> Enum.map(fn towel ->
            {:ok, regex} = (
                ("^" <> towel <> "(.*)$")
                |> debug(label: "regex1")
                |> Regex.compile()
                |> debug(label: "regex2")
            )
            {towel, regex}
        end)
    end

    def leafcount(tree) do
        tree
        |> List.flatten()
        |> Enum.filter(fn x -> x == :good_ending end)
        |> Enum.count()
    end

    def suffixset([]) do
        Map.new([{[], 0}])
    end
    def suffixset([head | tail]) do
        Map.put(suffixset(tail), [head | tail], 0)
    end
    def ps3_init(design, towels) do
        towellists = (
            towels
            |> Enum.map(fn towel ->
                towel
                |> String.split("", trim: true)
            end)
        )

        designlist = (
            design
            |> String.split("", trim: true)
        )

        suffixesmap = (
            Map.put(
                design
                |> String.split("", trim: true)
                |> suffixset(),
                designlist,
                1
            )
        )

        powersetscan3(
            designlist,
            suffixesmap,
            towellists
        )
    end

    def prefixmatch([], rest) do
        {:match, rest}
    end
    def prefixmatch(_, []) do
        {:no_match, nil}
    end
    def prefixmatch([h1 | shorter], [h2 | longer]) do
        # info({h1, h2}, label: "prefixmatch")
        # info({shorter, longer}, label: "prefixmatch")
        if h1 == h2 do
            prefixmatch(shorter, longer)
        else
            {:no_match, nil}
        end
    end

    def powersetscan3([], suffixestocheck, _towellists) do
        suffixestocheck[[]]
    end
    def powersetscan3(currentsuffix, suffixestocheck, towellists) do
        powersetscan3(
            currentsuffix
            |> tl(),
            (
                towellists
                |> Enum.reduce(suffixestocheck, fn towel, suffixestocheck ->
                    debug({towel, currentsuffix}, label: "powersetscan3")
                    case prefixmatch(towel, currentsuffix) do
                        {:match, rest} -> (
                            Map.put(
                                suffixestocheck,
                                rest,
                                suffixestocheck[rest] + suffixestocheck[currentsuffix]
                            ) |> debug(label: "match")
                        )
                        {:no_match, _} -> suffixestocheck
                    end
                end)
            ),
            towellists
        )
    end

    # def powersetscan2(designtogo, towelregexes) do
    #     towelregexes
    #     # |> debug(label: "regexes")
    #     |> Enum.map(fn {towel, towelre} ->
    #         case Regex.scan(towelre, designtogo) do
    #             [[_fullstr, ""]] -> 1
    #             [[_fullstr, rest]] -> powersetscan2(rest, towelregexes)
    #             [] -> 0
    #         end
    #         # |> debug(label: "result")
    #     end)
    #     |> Enum.sum()
    #     |> debug(label: "powersetscan2 out")
    # end

    def powersetscan(designtogo, towelregexes) do
        towelregexes
        # |> debug(label: "regexes")
        |> Enum.map(fn {towel, towelre} ->
            case Regex.scan(towelre, designtogo) do
                [[_fullstr, ""]] -> [towel, :good_ending]
                [[_fullstr, rest]] -> [towel | powersetscan(rest, towelregexes) ]
                [] -> :bad_ending
            end
            # |> debug(label: "result")
        end)
        |> Enum.filter(fn x -> x != :bad_ending end)
        |> debug(label: "powersetscan out")
    end

    # def runpart2_old({towels, designs}) do
    #     pregexes = prefixregexes(towels)
    #     {:ok, regex} = (
    #         ("^(" <> Enum.join(towels, "|") <> ")+$")
    #         |> debug(label: "regex1")
    #         |> Regex.compile()
    #         |> debug(label: "regex2")
    #     )

    #     designs
    #     |> Enum.map(fn design ->
    #         if Regex.match?(regex, design) do
    #             design
    #             |> info(label: "starting")
    #             |> powersetscan2(pregexes)
    #             |> info(label: "scan #{design}")
    #         else
    #             0
    #             |> info(label: "skip")
    #         end
    #     end)
    #     # |> leafcount()
    #     |> Enum.sum()
    # end

    def runpart2({towels, designs}) do
        designs
        |> Enum.map(fn design ->
            ps3_init(design, towels)
        end)
        |> Enum.sum()
    end
end


Puzzleday19.read_input("input/2024/day19inputtest.txt")
|> Puzzleday19.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzleday19.read_input("input/2024/day19input.txt")
|> Puzzleday19.runpart1()
|> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday19.read_input("input/2024/day19inputtest.txt")
|> Puzzleday19.runpart2()
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday19.read_input("input/2024/day19input.txt")
|> Puzzleday19.runpart2()
|> IO.inspect(pretty: true, label: "realinput, part2")
