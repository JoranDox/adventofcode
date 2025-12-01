defmodule Puzzleday21 do
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
    |> Enum.map(fn line -> line |> String.split("", trim: true) end)
    |> debug(label: "read_input 2")
    # |> Enum.map(
    #     fn line -> Enum.map(line, &String.to_integer/1) end
    # )
    |> debug(label: "read_input 3")
  end

  def prefixwithA(input) do
    input
    |> Enum.map(fn line -> ["A" | line] end)
  end

  # +---+---+---+
  # | 7 | 8 | 9 |
  # +---+---+---+
  # | 4 | 5 | 6 |
  # +---+---+---+
  # | 1 | 2 | 3 |
  # +---+---+---+
  #     | 0 | A |
  #     +---+---+

  #     +---+---+
  #     | ^ | A |
  # +---+---+---+
  # | < | v | > |
  # +---+---+---+
  def numpaddirpadmap() do
    %{
      "7" => {0, 0},
      "8" => {1, 0},
      "9" => {2, 0},
      "4" => {0, 1},
      "5" => {1, 1},
      "6" => {2, 1},
      "1" => {0, 2},
      "2" => {1, 2},
      "3" => {2, 2},
      "0" => {1, 3},
      "A" => {2, 3},
      # reusing the same A and moving to directional pad
      # this would be in the same position as 0 but they don't overlap
      "^" => {1, 3},
      "<" => {0, 4},
      "v" => {1, 4},
      ">" => {2, 4},
      :gap => {0, 3}
    }
  end

  # stolen from somewhere online, TODO: understand this
  def permutations([]), do: [[]]

  def permutations(list),
    do: for(elem <- list, rest <- permutations(list -- [elem]), do: [elem | rest])

  def options({from, to}) do
    debug({from, to}, label: "options in")
    {x1, y1} = numpaddirpadmap()[from]
    {x2, y2} = numpaddirpadmap()[to]

    horpart =
      case x2 - x1 do
        dx when dx > 0 -> List.duplicate([">"], dx)
        dx when dx < 0 -> List.duplicate(["<"], -dx)
        dx when dx == 0 -> []
      end
      |> debug(label: "options horpart")

    verpart =
      case y2 - y1 do
        dy when dy > 0 -> List.duplicate(["v"], dy)
        dy when dy < 0 -> List.duplicate(["^"], -dy)
        dy when dy == 0 -> []
      end
      |> debug(label: "options verpart")

    (horpart ++ verpart)
    |> List.flatten()
    |> debug(label: "options before permutations")
    |> permutations()
    |> debug(label: "options permutations")
    |> Enum.filter(fn option -> not hasgap?({x1, y1}, option) end)
  end

  def step({x, y}, dir) do
    case dir do
      ">" -> {x + 1, y}
      "<" -> {x - 1, y}
      "v" -> {x, y + 1}
      "^" -> {x, y - 1}
    end
  end

  def steps(head, []), do: [head]

  def steps(head, [direction | tail]) do
    nextstep = step(head, direction)
    [head | steps(nextstep, tail)]
  end

  def hasgap?(from, walk) do
    debug({from, walk}, label: "mindthegap in")
    Enum.any?(steps(from, walk), fn loc -> loc == numpaddirpadmap()[:gap] end)
  end

  def numpadmapset() do
    MapSet.new(["<", ">", "^", "v"])
  end

  def replace([from, to | tail]) do
    # debug([from, to | tail], label: "replace")
    {x1, y1} = numpaddirpadmap()[from]
    {x2, y2} = numpaddirpadmap()[to]

    horpart =
      case x2 - x1 do
        dx when dx > 0 -> List.duplicate([">"], dx)
        dx when dx < 0 -> List.duplicate(["<"], -dx)
        dx when dx == 0 -> []
      end

    verpart =
      case y2 - y1 do
        dy when dy > 0 -> List.duplicate(["v"], dy)
        dy when dy < 0 -> List.duplicate(["^"], -dy)
        dy when dy == 0 -> []
      end

    debug(horpart, label: "replace horpart")
    debug(verpart, label: "replace verpart")

    (if hasgap?({x1, y1}, (horpart ++ verpart) |> List.flatten()) do
       debug([from, to], label: "replace gap")
       verpart ++ horpart
     else
       horpart ++ verpart
     end ++
       ["A"] ++ replace([to | tail]))
    |> List.flatten()

    # if y2 > y1 do
    #   # from high to low
    #   if from in numpadmapset() or to in numpadmapset() do
    #     # dpad
    #     # debug([from, to], label: "replace hor first")
    #     verpart ++ horpart ++ ["A"] ++ replace([to | tail])
    #   else
    #     # numpad
    #     # debug([from, to], label: "replace ver first")
    #     horpart ++ verpart ++ ["A"] ++ replace([to | tail])
    #   end
    # else
    #   # same height or from low to high
    #   if from in numpadmapset() or to in numpadmapset() do
    #     # dpad
    #     # debug([from, to], label: "replace ver first")
    #     horpart ++ verpart ++ ["A"] ++ replace([to | tail])
    #   else
    #     # numpad
    #     # debug([from, to], label: "replace hor first")
    #     verpart ++ horpart ++ ["A"] ++ replace([to | tail])
    #   end
    # end
  end

  def replace(["A"]) do
    []
  end

  def replace2([from, to | tail]) do
    [
      case {from, to} do
        # A:^ = A<A
        {"A", "^"} -> ["A", "<", "A"]
        # A:> = AvA
        {"A", ">"} -> ["A", "v", "A"]
        # A:v = A<vA
        {"A", "v"} -> ["A", "<", "v", "A"]
        # A:< = Av<<A
        {"A", "<"} -> ["A", "v", "<", "<", "A"]
        # ^:A = A>A
        {"^", "A"} -> ["A", ">", "A"]
        # >:A = A^A
        {">", "A"} -> ["A", "^", "A"]
        # v:A = A>^A
        {"v", "A"} -> ["A", ">", "^", "A"]
        # <:A = A>>^A
        {"<", "A"} -> ["A", ">", ">", "^", "A"]
        # ^:> = never? (A>vA | Av>A)
        # or ["A", ">", "v", "A"]
        {"^", ">"} -> ["A", "v", ">", "A"]
        # ^:< = Av<A
        {"^", "<"} -> ["A", "v", "<", "A"]
        # >:^ = never? (A<^A | A^<A)
        # or ["A", "^", "<", "A"]
        {">", "^"} -> ["A", "<", "^", "A"]
        # >:v = A<A
        {">", "v"} -> ["A", "<", "A"]
        # v:> = A>A
        {"v", ">"} -> ["A", ">", "A"]
        # v:< = A<A
        {"v", "<"} -> ["A", "<", "A"]
        # <:^ = A>^A
        {"<", "^"} -> ["A", ">", "^", "A"]
        # <:v = A>A
        {"<", "v"} -> ["A", ">", "A"]
      end
      | replace2([to | tail])
    ]
  end

  def parsenum(line) do
    line
    |> Enum.filter(fn c -> c != "A" end)
    |> Enum.join("")
    |> String.to_integer()
  end

  def attempt2(input) do
    input
    |> debug(label: "attempt2 in")
    # |> prefixwithA()
    |> debug(label: "attempt2 prefix")
    |> Enum.map(fn line ->
      {
        line,
        Enum.zip(["A" | line], line)
        |> debug(label: "attempt2 zip")
        |> Enum.map(&options/1)
      }
    end)
    |> debug(label: "attempt2 out")
  end

  def attempt3(input) do
  end

  def runpart1(input) do
    attempt2(input)
  end

  def runpart1_old(input) do
    input
    # |> Task.async_stream(fn line -> {line, todo1(line)} end)
    # |> Enum.map(fn {:ok, result} -> result end)
    # |> Enum.map(fn line -> {line, todo1(line)} end)
    |> debug(label: "run0")
    |> Enum.map(fn origline ->
      {
        parsenum(origline),
        origline
      }
    end)
    |> debug(label: "run1")
    |> Enum.map(fn {origline, line} ->
      {
        origline,
        ["A" | line]
        |> replace()
      }
    end)
    |> debug(label: "run2")
    |> Enum.map(fn {origline, line} ->
      {
        origline,
        ["A" | line]
        |> replace()
      }
    end)
    |> debug(label: "run3")
    |> Enum.map(fn {origline, line} ->
      {
        origline,
        ["A" | line]
        |> replace()
      }
    end)
    |> debug(label: "run4", limit: :infinity)
    |> Enum.map(fn {origline, line} ->
      {
        origline,
        Enum.count(line)
      }
    end)
    |> debug(label: "run end")
    |> Enum.reduce(0, fn {origline, line}, acc -> acc + (line * origline) end)
  end

  def runpart2(input) do
    input
    # |> Enum.map(fn line -> {line, todo2(line)} end)
    |> debug(label: "run2")
    # |> Enum.count(fn {_line, sl} -> sl end)
    |> debug(label: "run3")
  end

  def test() do
    debug(steps({2,3}, ["<", "<", "^"]), label: "steps")
    debug(hasgap?({2,3}, ["<", "<", "^"]), label: "gap should be yes")
    debug(hasgap?({2,3}, ["<", "^"]), label: "gap should be no")
  end
end

Puzzleday21.test()

Puzzleday21.read_input("input/2024/day21inputtest.txt")
|> Puzzleday21.runpart1_old()
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzleday21.read_input("input/2024/day21input.txt")
|> Puzzleday21.runpart1_old()
|> IO.inspect(pretty: true, label: "realinput, part1")
# 218300 too high

# Puzzleday21.read_input("input/2024/day21inputtest.txt")
# |> Puzzleday21.runpart2()
# |> IO.inspect(pretty: true, label: "testinput, part2")

# Puzzleday21.read_input("input/2024/day21input.txt")
# |> Puzzleday21.runpart2()
# |> IO.inspect(pretty: true, label: "realinput, part2")
