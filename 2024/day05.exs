


defmodule Puzzleday05 do
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

    def testinput do
        read_input("input/2024/day05inputtest.txt")
    end

    def realinput do
        read_input("input/2024/day05input.txt")
    end

    def read_input(filename) do
        [rules, updates] = String.split(File.read!(filename), "\n\n", trim: true)
        %{
            :rules => String.split(rules, "\n", trim: true),
            :updates => String.split(updates, "\n", trim: true)
        }
        |> debug(label: "read_input 1")
    end

    def parserules(rules) do
       rules
        |> Enum.map(fn line -> String.split(line, "|", trim: true) end)
        |> debug(label: "parserules 1")

    end

    def parseupdate(updates) do
        updates
        |> Enum.map(fn line -> String.split(line, ",", trim: true) end)
        |> debug(label: "parseupdate 1")
    end

    def getmiddle(update) do
        # wa is deze vuile shit
        # String.to_integer(elem(List.to_tuple(update), (div((length(update)), 2))))
        String.to_integer(Enum.at(update, div((length(update)), 2)))
    end

    def checkrule(first, last, update) do
        case {first, last, update} do
            {:seen, last, [last | _]} -> true
            {first, :seen, [first | _]} -> false
            {first, _, [first | rest]} -> checkrule(:seen, last, rest)
            {_, last, [last | rest]} -> checkrule(first, :seen, rest)
            {_, _, [_ | rest]} -> checkrule(first, last, rest)
            {_, _, []} -> true
        end
    end

    def checkupdate(parsedrules, update) do
        parsedrules
        # |> Task.async_stream(fn [first, last] -> checkrule(first, last, update) end)
        # |> Enum.map(fn {:ok, result} -> result end)
        |> Enum.map(fn [first, last] -> checkrule(first, last, update) end)
        |> debug(label: "checkupdate 1")
        |> Enum.all?(fn x -> x end)
        |> then(fn x -> if x do getmiddle(update) else 0 end end) # this is ugly
        |> debug(label: "checkupdate 2")
    end

    def rules_to_dag(parsedrules) do
        parsedrules
        |> Enum.map(fn [first, last] -> {first, last} end)
        |> Enum.reduce(%{}, fn {first, last}, acc -> Map.put(acc, first, last) end)
    end

    def dag_to_chain_with_update(state, update) do
        debug(update, label: "entering dag_to_chain with update:")
        update_unique = MapSet.new(update)
        debug(update_unique, label: "used in updates")

        relevant_rules = Map.filter(state.rules_dag, fn {k, v} -> k in update_unique and v in update_unique end)
        debug(relevant_rules, label: "relevant_rules")

        keys_filtered = MapSet.new(Map.keys(relevant_rules))
        debug(keys_filtered, label: "inrules used in updates")
        values_filtered = MapSet.new(Map.values(relevant_rules))
        debug(values_filtered, label: "outrules used in updates")

        inrules_filtered = MapSet.difference(
            keys_filtered, values_filtered
        )
        debug(inrules_filtered, label: "inrules used in updates")
        outrules_filtered = MapSet.difference(
            values_filtered, keys_filtered
        )
        debug(outrules_filtered, label: "outrules used in updates")
        MapSet.size(inrules_filtered) == 1 or MapSet.size(outrules_filtered) == 1
    end

    def dag_to_chain(state) do
        keys = MapSet.new(Map.keys(state.rules_dag))
        values = MapSet.new(Map.values(state.rules_dag))
        inrules = MapSet.difference(keys, values)
        debug(inrules, label: "inrules")
        outrules = MapSet.difference(values, keys)
        debug(outrules, label: "outrules")
        updates_unique = MapSet.new(List.flatten(state.parsedupdates))
        debug(updates_unique, label: "used in updates")
        keys_filtered = MapSet.intersection(
            keys, updates_unique
        )
        debug(keys_filtered, label: "keys used in updates")
        values_filtered = MapSet.intersection(
            values, updates_unique
        )
        debug(values_filtered, label: "values used in updates")
        inrules_filtered = MapSet.difference(
            keys_filtered, values_filtered
        )
        debug(inrules_filtered, label: "inrules used in updates")
        outrules_filtered = MapSet.difference(
            values_filtered, keys_filtered
        )
        debug(outrules_filtered, label: "outrules used in updates")
        nil
    end


    def sort_by_partial_order(update, state) do
        Enum.sort(update,
            fn a, b -> [a,b] in state.parsedrules
            end
        )
    end


    def runpart1(state) do
        state
        |> Map.put(:parsedrules, parserules(state.rules))
        |> debug(label: "runpart1 1")
        |> Map.put(:parsedupdates, parseupdate(state.updates))
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        |> then(fn state ->
            state.parsedupdates
            |> Enum.map(fn update -> checkupdate(state.parsedrules, update) end)
            |> debug(label: "runpart1 2")
        end)
        |> debug(label: "runpart1 3")
        |> Enum.sum()
        |> debug(label: "runpart1 4")
    end

    def runpart2(state) do
        state
        |> Map.put(:parsedrules, parserules(state.rules))
        |> Map.put(:parsedupdates, parseupdate(state.updates))
        |> debug(label: "runpart2 1")
        # |> then(fn state ->
        #     state
        #     |> Map.put(:rules_dag, rules_to_dag(state.parsedrules))
        # end)
        |> then(& Map.put(&1, :rules_dag, rules_to_dag(&1.parsedrules)))
        |> debug(label: "runpart2 2")
        # |> then(fn state ->
        #     state.parsedupdates
        #     |> Enum.map(fn update -> dag_to_chain_with_update(state, update) end)
        # end)
        # |> then (fn state ->
        #     state
        #     |> Map.put(
        #         :answer,
        #         state.parsedupdates
        #         |> Enum.map(fn update -> {update, checkupdate(state.parsedrules, update)} end)
        #         |> Enum.map(fn {update, result} -> case result do
        #                 0 -> getmiddle(sort_by_partial_order(update, state))
        #                 _ -> 0
        #             end
        #         end
        #         )
        #     )
        # end)
        |> then (fn state ->
            state.parsedupdates
            |> Enum.map(fn update -> {update, checkupdate(state.parsedrules, update)} end)
            |> debug(label: "runpart2_inside_then 1")
            |> Enum.map(fn {update, result} ->
                case result do
                    0 -> getmiddle(sort_by_partial_order(update, state))
                    _ -> 0
                end
            end)
        end)
        |> debug(label: "runpart2 3")
        |> debug(label: "runpart2 4")
        # |> then(fn state -> state.rules_dag end)
        # |> debug(label: "runpart2 3", limit: :infinity)
        # |> debug(label: "runpart2 3")
        # |> Enum.map(fn line -> {line, todo2(line)} end)
        # |> debug(label: "run2")
        # |> Enum.count(fn {_line, sl} -> sl end)
        # |> debug(label: "run3")
    end
end

# Puzzleday05.testinput()
# |> Puzzleday05.runpart1()
# |> IO.inspect(pretty: true, label: "testinput, part1")

# Puzzleday05.realinput()
# |> Puzzleday05.runpart1()
# |> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday05.testinput()
|> Puzzleday05.runpart2()
# |> debug(label: "afterthatstuff")
|> Enum.sum()
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday05.realinput()
|> Puzzleday05.runpart2()
|> Enum.sum()
|> IO.inspect(pretty: true, label: "realinput, part2")
