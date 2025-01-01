defmodule Puzzleday24 do
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

  defp info(msg, opts, force \\ false) do
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
    [input, gates] =
      File.read!(filename)
      |> String.split("\n\n", trim: true)
      |> debug(label: "read_input 1")

    # e.g. x03: 1

    input =
      input
      |> debug(label: "read_input input 0")
      |> String.split("\n", trim: true)
      |> debug(label: "read_input input 1")
      |> Enum.map(fn line ->
        String.split(line, ": ", trim: true)
      end)
      |> Enum.map(fn [a, b] ->
        case b do
          # or do we want to use 0 and 1?
          "0" -> {a, false}
          "1" -> {a, true}
        end
      end)
      |> Enum.into(%{})
      |> debug(label: "read_input input")

    # e.g. x00 OR x03 -> fst
    gatesregex = ~r/(\w\w\w) (OR|XOR|AND) (\w\w\w) -> (\w\w\w)/

    gates =
      gates
      |> debug(label: "read_input gates 0")
      |> String.split("\n", trim: true)
      |> debug(label: "read_input gates 1")
      |> Enum.map(fn string -> Regex.scan(gatesregex, string) end)
      |> debug(label: "read_input gates 2")
      |> Enum.map(fn [[_, arg1, op, arg2, result]] ->
        {result, {arg1, op, arg2}}
      end)
      |> Enum.into(%{})
      |> debug(label: "read_input gates")

    {input, gates}
  end

  def getwires(gates, which \\ "z") do
    gates
    |> Map.keys()
    |> Enum.filter(fn wire -> String.starts_with?(wire, which) end)
    |> Enum.sort(:desc)
  end

  def operategate(arg1, op, arg2) do
    case op do
      "AND" -> arg1 && arg2
      "OR" -> arg1 || arg2
      "XOR" -> arg1 != arg2
    end
  end

  # def computewire(wire, gates, input) do
  #     case input[wire] do
  #         nil -> (
  #             {arg1, op, arg2} = gates[wire]
  #             {gates, input} = computewire(arg1, gates, input)
  #             {gates, input} = computewire(arg2, gates, input)
  #             input = Map.put(input, wire, operategate({arg1, op, arg2}, input))
  #         )
  #         other -> other
  #     end
  # end

  def fillwires(input, gates) do
    # do a pass over the gates to fill in the value of any wire that can now be filled in
    newinput =
      gates
      |> Enum.reduce(input, fn {wire, {arg1, op, arg2}}, acc ->
        case {acc[arg1], acc[arg2]} do
          {nil, _} -> acc
          {_, nil} -> acc
          {v1, v2} -> Map.put(acc, wire, operategate(v1, op, v2))
        end
      end)
      |> debug(label: "fillwires 1")

    # nothing changed
    if newinput == input do
      newinput
    else
      fillwires(newinput, gates)
    end
  end

  def wirestonum(wires, input) do
    wires
    |> debug(label: "wirestonum in")
    |> Enum.reduce(0, fn wire, acc ->
      (acc * 2 + if input[wire], do: 1 |> info(label: "wirestonum 1 #{acc}"), else: 0 |> info(label: "wirestonum 0 #{acc}"))
      |> info(label: "wirestonum step")
    end)
  end

  def runpart1({input, gates}) do
    allwires =
      fillwires(input, gates)
      # |> Task.async_stream(fn line -> {line, todo1(line)} end)
      # |> Enum.map(fn {:ok, result} -> result end)
      # |> Enum.map(fn line -> {line, todo1(line)} end)
      |> debug(label: "run2")

    allwires
    |> getwires("z")
    # |> Enum.reverse()
    |> wirestonum(allwires)
    # |> Enum.count(fn {_line, sl} -> sl end)
    |> debug(label: "run3")
  end

  def tobinary(num) do
    num
    |> Integer.to_string(2)
  end

  def newinput(input, letter, number) do
    numdigits = (
      input
      |> getwires(letter)
      |> Enum.count()
    )

    number
    |> tobinary()
    # |> debug(label: "newinput 0") # 1 -> 1, 2 -> 10, 3 -> 11, 4 -> 100 etc
    # don't forget to pad with 0s
    |> String.pad_leading(numdigits, "0") # 1 -> 001, 2 -> 010, 3 -> 011, 4 -> 100 etc
    |> String.reverse() # 1 -> 100, 2 -> 010, 3 -> 110, 4 -> 001 etc
    |> String.split("", trim: true)
    |> Enum.with_index() # thanks to the reverse, index 0 is the least significant bit
    # |> debug(label: "newinput 1")
    |> Enum.map(fn {bit, i} -> {letter <> String.pad_leading("#{i}", 2, "0"), bit == "1"} end)
    |> debug(label: "newinput")
    |> Enum.into(input)

  end


  def runpart2({input, gates}) do
    x =
      input
      |> getwires("x")
      # |> Enum.reverse()
      |> then(fn wires ->
        wires
        |> Enum.map(fn wire -> {wire, input[wire]} end)
        |> info(label: "x as binary")
        wires
      end)
      |> wirestonum(input)

    y =
      input
      |> getwires("y")
      # |> Enum.reverse()
      |> then(fn wires ->
        wires
        |> Enum.map(fn wire -> {wire, input[wire]} end)
        |> info(label: "y as binary")
        wires
      end)
      |> wirestonum(input)

    # x = 1
    # input = newinput(input, "x", x)

    # y = 2 ** 16 - 1
    # input = newinput(input, "y", y)

    # x =
    #   input
    #   |> getwires("x")
    #   # |> Enum.reverse()
    #   |> debug(label: "x")
    #   |> then(fn wires ->
    #     wires
    #     |> Enum.map(fn wire -> {wire, input[wire]} end)
    #     |> info(label: "x as binary")
    #     wires
    #   end)
    #   |> wirestonum(input)

    # y =
    #   input
    #   |> getwires("y")
    #   # |> Enum.reverse()
    #   |> then(fn wires ->
    #     wires
    #     |> Enum.map(fn wire -> {wire, input[wire]} end)
    #     |> info(label: "y as binary")
    #     wires
    #   end)
    #   |> wirestonum(input)


    z = runpart1({input, gates})

    debug({x, y, z, x + y, Bitwise.bxor(x + y,  z), tobinary(Bitwise.bxor(x + y,  z))}, label: "run1")
    # |> Enum.map(fn line -> {line, todo2(line)} end)
    |> debug(label: "run2")
    # |> Enum.count(fn {_line, sl} -> sl end)
    |> debug(label: "run3")
  end
end

# Puzzleday24.read_input("input/2024/day24inputtest.txt")
# |> Puzzleday24.runpart1()
# |> IO.inspect(pretty: true, label: "testinput, part1")

# Puzzleday24.read_input("input/2024/day24input.txt")
# |> Puzzleday24.runpart1()
# |> IO.inspect(pretty: true, label: "realinput, part1")

# Puzzleday24.read_input("input/2024/day24inputtest.txt")
# |> Puzzleday24.runpart2()
# |> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday24.read_input("input/2024/day24input_corrected.txt")
|> Puzzleday24.runpart2()
|> IO.inspect(pretty: true, label: "realinput, part2")
