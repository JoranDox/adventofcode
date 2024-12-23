


defmodule Puzzleday23 do
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

    def read_input(filename) do
        File.read!(filename)
        |> String.split("\n", trim: true)
        |> debug(label: "read_input 1")
        |> Enum.map(fn line -> line |> String.split("-") end)
        |> debug(label: "read_input 2")
        |> Enum.map(fn [a, b] -> [{a, b}, {b, a}] end)
        # |> Enum.map(fn [a, b] -> {a, b} end)
        |> debug(label: "read_input 3")
        |> List.flatten()
        |> debug(label: "read_input 4", limit: :infinity)
        |> MapSet.new()
    end

    def getallcomputers(netgraph) do
        netgraph
        |> Enum.map(fn {a, b} -> a end)
        |> MapSet.new()
    end

    def findneighbours(computer, netgraph) do
        netgraph
        |> Enum.filter(fn {a, _b} -> a == computer end)
        |> Enum.map(fn {_a, b} -> b end)
        |> MapSet.new()
    end

    def findtrigraphs(computer, neighbours, netgraph) do
        neighbours
        |> Enum.map(fn neighbour ->
            findneighbours(neighbour, netgraph)
            |> Enum.map(fn neighbourneighbour ->
                {computer, neighbour, neighbourneighbour}
            end)
        end)
        |> List.flatten()
        |> Enum.filter(fn {c, n1, n2} -> n2 in neighbours end)
        |> Enum.map(fn {c, n1, n2} -> MapSet.new([c, n1, n2]) end)
        |> debug(label: "findtrigraphs #{computer} out")
    end

    def counter(enum) do
        enum
        |> Enum.reduce(%{}, fn x, acc -> Map.update(acc, x, 1, &(&1 + 1)) end)
    end

    def pairs(set) do
        set
        |> Enum.map(fn x  ->
            set
            |> Enum.map(fn y -> {x, y} end)
        end)
        |> List.flatten()
        |> Enum.filter(fn {a,b} -> a != b end)
    end

    def setisclique?(set, netgraph) do
        # allsubsets(set)
        # # this is probably not the most efficient way =)
        # |> Enum.filter(fn subset -> MapSet.size(subset) == 2 end)
        # |> MapSet.to_list()
        # |> Enum.map(fn [a,b] -> {a,b} end)
        (
            pairs(set)
            |> debug(label: "setisclique? pairs")
            |> Enum.filter(fn {a,b} -> {a,b} not in netgraph end)
            |> length()
        ) == 0
    end

    def allsubsets(set) do
        MapSet.new(allsubsetshelper(set, MapSet.new([set, MapSet.new()])))
        |> MapSet.to_list()
        |> debug(label: "allsubsets out")
    end
    def allsubsetshelper(set, seen) do
        [
            set |
            set
            # |> debug(label: "allsubsets in")
            |> then(fn set ->
                case MapSet.size(set) do
                    # 0 -> [] # shouldn't be possible since I added seen
                    1 -> [set]
                    _ -> (
                        set
                        |> Enum.map(fn x -> MapSet.delete(set, x) end)
                        # |> debug(label: "allsubsets 1")
                        |> Enum.filter(fn x -> x not in seen end)
                        |> Enum.map(fn x -> allsubsetshelper(x, MapSet.put(seen, x)) end)
                        # |> debug(label: "allsubsets combo")
                        |> List.flatten()
                        # |> debug(label: "allsubsets flatten")
                        |> Enum.filter(fn x -> MapSet.size(x) > 0 end)
                        # |> debug(label: "allsubsets filtered")
                    )
                end
            end)
        ]
        # |> debug(label: "allsubsets pre out")
        # |> MapSet.new()

    end

    def findlargestclique1(netgraph, size \\ nil) do
        compneighs = (
            netgraph
            |> getallcomputers()
            |> Enum.map(fn computer -> MapSet.put(findneighbours(computer, netgraph), computer) end)
            |> debug(label: "findlargestclique all neighs")
            )

        compneighs
        |> Enum.map(fn neighset -> allsubsets(neighset) end)
        |> List.flatten()
        |> MapSet.new()
        |> MapSet.to_list() # is there a better unique?
        |> debug(label: "findlargestclique allsubsets")
        |> Enum.sort(fn a, b -> MapSet.size(a) > MapSet.size(b) end)
        |> debug(label: "findlargestclique sorted")
        |> Enum.reduce_while(nil, fn subset, nil ->
            if setisclique?(MapSet.new(subset), netgraph) do
                {:halt, subset}
            else
                {:cont, nil}
            end
        end)
        # {neighhigh, highest} = (
        #     compneighsizes
        #     |> Enum.max_by(fn {neighbours, size} -> size end)
        #     |> debug(label: "findlargestclique max")
        # )

        # size = if size == nil do
        #     highest
        # else
        #     size
        # end

        # counted = (
        #     compneighsizes
        #     # |> Enum.filter(fn {neighbours, size} -> size >= highest end)
        #     # |> debug(label: "findlargestclique")
        #     |> counter()
        #     |> debug(label: "findlargestclique counter")
        # )



    end

    def findlargestclique2(netgraph, size \\ nil) do
        netgraph
        |> getallcomputers()
        |> allsubsets()
        |> List.flatten()
        |> MapSet.new()
        |> MapSet.to_list() # is there a better unique?
        |> debug(label: "findlargestclique2 allsubsets")
        |> Enum.sort(fn a, b -> MapSet.size(a) > MapSet.size(b) end)
        |> debug(label: "findlargestclique2 sorted")
        |> Enum.reduce_while(nil, fn subset, nil ->
            if setisclique?(MapSet.new(subset), netgraph) do
                {:halt, subset}
            else
                {:cont, nil}
            end
        end)
    end

    def etsput(clique) do
        :ets.insert(:cliques, {clique, nil}) # key and value are the same
    end
    def etsgetcliques() do
        :ets.match_object(:cliques, :"$1")
        # gives a list of {clique, nil}, ... tuples
        |> Enum.map(fn {clique, _} -> clique end)
    end

    def bronkerboschwithpivot(netgraph, p, r \\ MapSet.new(), x \\ MapSet.new()) do
        # algorithm BronKerbosch1(P, R, X) is
        #     if P and X are both empty then
        #         report R as a maximal clique
        #     for each vertex v in P do
        #         BronKerbosch1(P ⋂ N(v), R ⋃ {v}, X ⋂ N(v))
        #         P := P \ {v}
        #         X := X ⋃ {v}

        # algorithm BronKerbosch2(P, R, X) is
        #     if P and X are both empty then
        #         report R as a maximal clique
        #     choose a pivot vertex u in P ⋃ X
        #     for each vertex v in P \ N(u) do
        #         BronKerbosch2(P ⋂ N(v), R ⋃ {v}, X ⋂ N(v))
        #         P := P \ {v}
        #         X := X ⋃ {v}
        debug({p, r, x}, label: "BK in")
        if p == MapSet.new() and x == MapSet.new() do
            etsput(
                r |> debug(label: "maximal clique")
            )
        end
        u = Enum.at(MapSet.union(p, x), 0)
        uneighs = findneighbours(u, netgraph) |> debug(label: "neighbours of pivot #{u} (N(u))")
        pwithoutuneighs = MapSet.difference(p, uneighs) |> debug(label: "P \\ N(u)")

        pwithoutuneighs
        |> Enum.reduce({p, x}, fn v, {p, x} ->
            vneighs = findneighbours(v, netgraph) |> debug(label: "neighbours of v #{v} (N(v))")

            bronkerboschwithpivot(
                netgraph,
                MapSet.intersection(p, vneighs),
                MapSet.put(r, v),
                MapSet.intersection(x, vneighs)
            )

            {MapSet.delete(p, v), MapSet.put(x, v)}

        end)
        nil
    end


    def runpart1(netgraph) do
        netgraph
        |> getallcomputers()
        |> debug(label: "run1")
        |> Enum.filter(fn computer -> String.starts_with?(computer, "t") end)
        |> Enum.map(fn computer -> {computer, findneighbours(computer, netgraph)} end)
        |> debug(label: "run2")
        |> Enum.map(fn {computer, neighbours} -> findtrigraphs(computer, neighbours, netgraph) end)
        |> debug(label: "run3")
        |> List.flatten()
        |> debug(label: "run4")
        |> MapSet.new()
        |> debug(label: "run5")
        # |> Enum.filter(fn {computer, neighbours} -> MapSet.size(neighbours) > 0 end)
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        # |> Enum.map(fn line -> {line, todo1(line)} end)
        # |> debug(label: "run2")
        # |> Enum.count(fn {_line, sl} -> sl end)
        |> MapSet.size()
    end

    def runpart2(input) do
        input
        # |> findlargestclique2()
        |> bronkerboschwithpivot(getallcomputers(input))
        # |> Enum.map(fn line -> {line, todo2(line)} end)
        etsgetcliques()
        |> debug(label: "run2")
        |> Enum.max_by(fn clique -> MapSet.size(clique) end)
        # |> Enum.count(fn {_line, sl} -> sl end)
        |> debug(label: "run3")
        |> Enum.join(",")
    end
end

:ets.new(:cliques, [:public, :named_table])
[1, 1, 1, 1, 1, 2, 2, 2, 3]
|> Puzzleday23.counter()
|> IO.inspect(pretty: true, label: "counter")

MapSet.new([1, 1, 1, 1, 1, 2, 2, 2, 3])
|> Puzzleday23.allsubsets()
|> IO.inspect(pretty: true, label: "allsubsets")

Puzzleday23.setisclique?(
    MapSet.new([1, 2, 3]),
    MapSet.new([{1, 2}, {2, 3}, {1, 3}, {2, 1}, {3, 1}, {3, 2}])
)
|> IO.inspect(pretty: true, label: "setisclique?")

Puzzleday23.setisclique?(
    MapSet.new([1, 2, 3]),
    MapSet.new([{1, 2}, {1, 3}, {2, 1}, {3, 1}, {3, 2}])
)
|> IO.inspect(pretty: true, label: "setisclique?")

# Puzzleday23.read_input("input/2024/day23inputtest.txt")
# |> Puzzleday23.runpart1()
# |> IO.inspect(pretty: true, label: "testinput, part1")

# Puzzleday23.read_input("input/2024/day23input.txt")
# |> Puzzleday23.runpart1()
# |> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday23.read_input("input/2024/day23inputtest.txt")
|> Puzzleday23.runpart2()
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday23.read_input("input/2024/day23input.txt")
|> Puzzleday23.runpart2()
|> IO.inspect(pretty: true, label: "realinput, part2")
