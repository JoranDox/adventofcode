


defmodule Puzzleday12 do
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
        read_input("input/2024/day12inputtest.txt")
    end

    def testinput_E do
        read_input("input/2024/day12inputtest_E.txt")
    end


    def realinput do
        read_input("input/2024/day12input.txt")
    end

    def neighbours({x,y}, direction) do
        horizontal = [
            {x+1, y},
            {x-1, y},
        ]
        vertical = [
            {x, y+1},
            {x, y-1}
        ]
        case direction do
            :all -> horizontal ++ vertical
            :horizontal -> horizontal
            :vertical -> vertical
        end
    end

    def borders(mapset) do
        mapset
        |> Enum.map(fn loc -> neighbours(loc, :all) end)
        |> List.flatten()
        |> Enum.filter(fn loc -> loc not in mapset end)
    end

    def scorep1(mapset) do
        # score is area * perimeter
        (
            borders(mapset)
            |> info(label: "scorep1 borders")
            # this is the borders of a given mapset I believe
            # which also means it's the length of the border
            |> Enum.count()
        )
        *
        MapSet.size(mapset)
    end

    def to_sorted_list(mapset) do
        mapset
        |> Enum.to_list()
        |> Enum.sort(fn {x1,y1}, {x2,y2} -> if y1 == y2 do x1 < x2 else y1 < y2 end end)
    end

    def find_index(list, fun) do
        info(list, label: "find_index list")
        max(
            Enum.find_index(list, fun) || length(list) +1,
            1
        )
        |> info(label: "find_index out")
    end

    def get_valid_chunk(border, initial_loc, area, :above) do
        border
        |> Enum.chunk_by(fn {x,y} -> {x,y-1} in area end)
        |> Enum.filter(fn x -> initial_loc in x end)
        |> Enum.at(0) # should only have one chunk really
        |> Enum.filter(fn {x,y} -> {x,y-1} in area end)
    end
    def get_valid_chunk(border, initial_loc, area, :below) do
        border
        |> Enum.chunk_by(fn {x,y} -> {x,y+1} in area end)
        |> Enum.filter(fn x -> initial_loc in x end)
        |> Enum.at(0) # should only have one chunk really
        |> Enum.filter(fn {x,y} -> {x,y+1} in area end)
    end
    def get_valid_chunk(border, initial_loc, area, :left) do
        border
        |> Enum.chunk_by(fn {x,y} -> {x-1,y} in area end)
        |> Enum.filter(fn x -> initial_loc in x end)
        |> Enum.at(0) # should only have one chunk really
        |> Enum.filter(fn {x,y} -> {x-1,y} in area end)
    end
    def get_valid_chunk(border, initial_loc, area, :right) do
        border
        |> Enum.chunk_by(fn {x,y} -> {x+1,y} in area end)
        |> Enum.filter(fn x -> initial_loc in x end)
        |> Enum.at(0) # should only have one chunk really
        |> Enum.filter(fn {x,y} -> {x+1,y} in area end)
    end

    def scorep2(mapset) do
        (
            mapset
            |> info(label: "scorep2 input (mapset)")
            |> borders()
            |> debug(label: "scorep2 borders")
            |> then(fn map -> # because we need to name map for the floodfill
                map
                |> Task.async_stream(fn loc ->
                    {
                        loc,
                        floodfill(map, loc, MapSet.new([loc]), :horizontal) |> to_sorted_list(),
                        floodfill(map, loc, MapSet.new([loc]), :vertical) |> to_sorted_list()
                    }
                end)
                |> Enum.map(fn {:ok, result} -> result end)
            end)
            |> info(label: "scorep2 all borders")
            |> Enum.map(
                fn {loc, horizontal, vertical} ->
                    [
                        {get_valid_chunk(horizontal, loc, mapset, :above), :above},
                        {get_valid_chunk(horizontal, loc, mapset, :below), :below},
                        {get_valid_chunk(vertical, loc, mapset, :left), :left},
                        {get_valid_chunk(vertical, loc, mapset, :right), :right}
                        # {
                        #     Enum.slice(
                        #         horizontal |> info(label: "horizontal"),
                        #         0,
                        #         find_index(
                        #             horizontal,
                        #             fn {vx,vy} -> {vx,vy+1} not in mapset end
                        #         )-1 |> info(label: "find_index 1")
                        #     ),
                        #     :below
                        # },
                        # {Enum.slice(horizontal, 0, find_index(horizontal, fn {vx,vy} -> {vx,vy-1} not in mapset end)-1), :above},
                        # {Enum.slice(vertical, 0, find_index(vertical, fn {hx,hy} -> {hx+1,hy} not in mapset end)-1), :right},
                        # {Enum.slice(vertical, 0, find_index(vertical, fn {hx,hy} -> {hx-1,hy} not in mapset end)-1), :left}
                        # {Enum.filter(horizontal, fn {vx,vy} -> {vx,vy+1} in mapset end), :below},
                        # {Enum.filter(horizontal, fn {vx,vy} -> {vx,vy-1} in mapset end), :above},
                        # {Enum.filter(vertical, fn {hx,hy} -> {hx+1,hy} in mapset end), :right},
                        # {Enum.filter(vertical, fn {hx,hy} -> {hx-1,hy} in mapset end), :left}
                    ]
                end
            )
            |> info(label: "scorep2 candidates")
            |> List.flatten()
            |> info(label: "scorep2 after flatten")
            |> Enum.filter(fn {maplist, _where} -> length(maplist) > 0 end)
            |> info(label: "scorep2 after filtering empty")
            |> Enum.map(fn {maplist, where} -> length(maplist) |> debug(label: "sizes 1"); {maplist, where} end)
            |> MapSet.new() # combine them
            |> info(label: "scorep2 unique")
            |> Enum.map(fn {maplist, where} -> length(maplist) |> debug(label: "sizes 2"); {maplist, where} end)
            |> info(label: "scorep2 borders cleaned")
            |> Enum.count()
        ) * MapSet.size(mapset)
        |> debug(label: "scorep2 final")
    end

    def mapprint(loc, map) do
        {loc, Map.get(map, loc)}
        |> debug(label: "mapprint")
        loc
    end

    def listofliststomap(listoflists) do
        listoflists
        |> Enum.with_index()
        |> Enum.map( fn {line, yindex} ->
            line
            |> Enum.with_index()
            |> Enum.map( fn {char, xindex} ->
                case char do
                    node -> {{xindex, yindex}, node}
                end
            end)
        end)
        |> List.flatten()
        |> Enum.filter(fn x -> x != nil end)
        |> Map.new()
    end

    def read_input(filename) do
        File.read!(filename)
        |> String.split("\n", trim: true)
        |> debug(label: "read_input 1")
        |> Enum.map(fn line -> line |> String.split("", trim: true) end)
        |> debug(label: "read_input 2")
        |> debug(label: "read_input 3")
    end

    def typefilter(locs, map, comparison, direction) do
        case direction do
            :all -> locs |> Enum.filter(fn loc -> map[loc] == map[comparison] end)
            _ -> locs |> Enum.filter(fn loc -> loc in map end)
        end
    end

    def floodfill(map, loc, accum, direction \\ :all) do
        loc
        |> debug(label: "floodfill in")
        # |> mapprint(map)
        |> neighbours(direction)
        |> debug(label: "floodfill neighbours")
        # |> Enum.map(fn loc -> loc |> mapprint(map) end)
        |> typefilter(map, loc, direction) # same type
        |> debug(label: "floodfill filter type")
        |> Enum.filter(fn neighbour -> neighbour not in accum end) # unseen
        |> debug(label: "floodfill filter seen")
        |> Enum.reduce(accum, fn neighbour, accum ->
            floodfill(map, neighbour, MapSet.union(accum, MapSet.new([loc, neighbour])), direction)
        end)
        |> debug(label: "floodfill out")
    end

    def common(input) do
        input
        |> debug(label: "run0")
        |> listofliststomap()
        |> debug(label: "run1")
        |> then(fn map -> # because we need to name map for the floodfill
            map
            |> Task.async_stream(fn {k,_v} ->
                floodfill(map, k, MapSet.new([k]))
            end)
            |> Enum.map(fn {:ok, result} -> result end)
        end)
        |> Enum.map(fn mapset -> MapSet.size(mapset) |> debug(label: "sizes 1"); mapset end)
        |> MapSet.new() # combine them
        |> Enum.map(fn mapset -> MapSet.size(mapset) |> debug(label: "sizes 2"); mapset end)
        |> debug(label: "run 5")
    end
    def runpart1(mapsetset, whichinput) do
        mapsetset
        |> Enum.map(fn mapset -> mapset |> scorep1 end)
        |> Enum.sum()
        |> IO.inspect(pretty: true, label: "#{whichinput}, part1")
        mapsetset
    end

    def runpart2(mapsetset, whichinput) do
        mapsetset
        |> debug(label: "runpart2 1")
        |> Enum.map(fn mapset -> mapset |> scorep2 end)
        |> debug(label: "runpart2 2")
        |> Enum.sum()
        |> IO.inspect(pretty: true, label: "#{whichinput}, part2")
        mapsetset
    end
end

Puzzleday12.read_input("input/2024/day12inputtest_mini.txt")
|> Puzzleday12.common()
|> Puzzleday12.runpart1("testinput_mini") # 8 borderlength, 3 squares = 24
|> Puzzleday12.runpart2("testinput_mini") # 6 borders, 3 squares = 18

Puzzleday12.read_input("input/2024/day12inputtest_small.txt")
|> Puzzleday12.common()
|> Puzzleday12.runpart1("testinput_small") # 140
|> Puzzleday12.runpart2("testinput_small") # 80

Puzzleday12.read_input("input/2024/day12inputtest_medium.txt")
|> Puzzleday12.common()
|> Puzzleday12.runpart1("testinput_medium") # 1184?
|> Puzzleday12.runpart2("testinput_medium") # 368

Puzzleday12.testinput_E()
|> Puzzleday12.common()
|> Puzzleday12.runpart1("testinput_E") # 692?
|> Puzzleday12.runpart2("testinput_E") # 236

Puzzleday12.testinput()
|> Puzzleday12.common()
|> Puzzleday12.runpart1("testinput") # 1930
|> Puzzleday12.runpart2("testinput") # 1206


Puzzleday12.realinput()
|> Puzzleday12.common()
|> Puzzleday12.runpart1("realinput") # 1396562
|> Puzzleday12.runpart2("realinput") # 844132
