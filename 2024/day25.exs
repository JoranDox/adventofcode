defmodule Puzzleday25 do
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

  def keyorhole(key) do
    case key do
      ["#####" | _rest] -> :hole
      _rest -> :key
    end
  end

  def readkey(key) do
    key
    |> debug(label: "readkey in")
    |> Enum.map(fn line ->
      String.split(line, "", trim: true)
    end)
    # transpose
    |> Enum.zip_with(&Function.identity/1)
    |> debug(label: "readkey transpose")
    |> Enum.map(fn keycol ->
      keycol
      |> Enum.count(fn x -> x == "#" end)
    end)
    |> debug(label: "readkey out")
  end

  def keymatch?(key, hole) do
    key
    |> Enum.zip(hole)
    |> Enum.map(fn {k, h} -> k + h < 8 end)
    |> Enum.all?()
    |> debug(label: "match")
  end

  def read_input(filename) do
    File.read!(filename)
    |> String.split("\n\n", trim: true)
    |> debug(label: "read_input 1")
    |> Enum.reduce({[], []}, fn thing, {keys, keyholes} ->
      thing
      |> String.split("\n", trim: true)
      |> debug(label: "read_input thing")
      |> then(fn key ->
        case {keyorhole(key), readkey(key)} do
          {:key, rest} -> {keys, [rest | keyholes]}
          {:hole, rest} -> {[rest | keys], keyholes}
        end
      end)
      |> debug(label: "read_input reduce")
    end)
    |> debug(label: "read_input 2")
  end

  def runpart1({keys, holes}) do
    keys
    |> Enum.map(fn key ->
        holes
        |> Enum.map(fn hole -> {key, hole, keymatch?(key, hole)} end)
    end)
    # |> Task.async_stream(fn line -> {line, todo1(line)} end)
    # |> Enum.map(fn {:ok, result} -> result end)
    # |> Enum.map(fn line -> {line, todo1(line)} end)
    |> debug(label: "run2")
    |> List.flatten()
    # |> Enum.count(fn {_line, sl} -> sl end)
    |> debug(label: "run3")
    |> Enum.count(fn {_, _, sl} -> sl end)
  end

  def runpart2(input) do
    input
    # |> Enum.map(fn line -> {line, todo2(line)} end)
    |> debug(label: "run2")
    # |> Enum.count(fn {_line, sl} -> sl end)
    |> debug(label: "run3")
  end
end

Puzzleday25.read_input("input/2024/day25inputtest.txt")
|> Puzzleday25.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzleday25.read_input("input/2024/day25input.txt")
|> Puzzleday25.runpart1()
|> IO.inspect(pretty: true, label: "realinput, part1")

# Puzzleday25.read_input("input/2024/day25inputtest.txt")
# |> Puzzleday25.runpart2()
# |> IO.inspect(pretty: true, label: "testinput, part2")

# Puzzleday25.read_input("input/2024/day25input.txt")
# |> Puzzleday25.runpart2()
# |> IO.inspect(pretty: true, label: "realinput, part2")
