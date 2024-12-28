defmodule Puzzleday17 do
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
    regex = ~r/Register A: (\d+)\nRegister B: 0\nRegister C: 0\n\nProgram: ((?:\d,?)+(?:\d))$/
    inputstring = File.read!(filename)

    [regA, program] =
      Regex.scan(regex, inputstring)
      |> debug(label: "read_input 1")
      # only one match
      |> hd()
      # remove the first match, which is the whole match
      |> tl()

    {
      {String.to_integer(regA), 0, 0, 0},
      program
      |> String.split(",")
      |> Enum.map(&String.to_integer/1)
      |> Enum.with_index()
      |> Enum.map(fn {instruction, ip} -> {ip, instruction} end)
      |> Map.new()
      |> Map.put(:out, [])
      |> Map.put(
        :program,
        program
        |> String.split(",")
        |> Enum.map(&String.to_integer/1)
      )
    }
  end

  def combooperand({a, b, c, ip}, program) do
    case program[ip + 1] do
      0 -> 0
      1 -> 1
      2 -> 2
      3 -> 3
      4 -> a
      5 -> b
      6 -> c
    end
  end

  def literaloperand({_a, _b, _c, ip}, program) do
    program[ip + 1]
  end

  def adv({{a, b, c, ip}, program}) do
    # division of A by 2 to the power of the combo operand, stored in A
    debug({a, b, c, ip}, label: "adv")
    {{div(a, 2 ** combooperand({a, b, c, ip}, program)), b, c, ip + 2}, program}
  end

  def bdv({{a, b, c, ip}, program}) do
    # division of A by 2 to the power of the combo operand, stored in B
    debug({a, b, c, ip}, label: "bdv")
    {{a, div(a, 2 ** combooperand({a, b, c, ip}, program)), c, ip + 2}, program}
  end

  def cdv({{a, b, c, ip}, program}) do
    # division of A by 2 to the power of the combo operand, stored in C
    debug({a, b, c, ip}, label: "cdv")
    {{a, b, div(a, 2 ** combooperand({a, b, c, ip}, program)), ip + 2}, program}
  end

  def bxl({{a, b, c, ip}, program}) do
    # bitwise xor of register B and literal operand, stored in B
    debug({a, b, c, ip}, label: "bxl")
    {{a, Bitwise.bxor(b, literaloperand({a, b, c, ip}, program)), c, ip + 2}, program}
  end

  def bst({{a, b, c, ip}, program}) do
    # combo operand modulo 8 to B register
    debug({a, b, c, ip}, label: "bst")
    {{a, combooperand({a, b, c, ip}, program) |> Integer.mod(8), c, ip + 2}, program}
  end

  def jnz({{a, b, c, ip}, program}) do
    # if the A register is not zero, jump to the literal operand
    debug({a, b, c, ip}, label: "jnz")

    case a do
      0 -> {{a, b, c, ip + 2}, program}
      _ -> {{a, b, c, literaloperand({a, b, c, ip}, program)}, program}
    end
  end

  def bxc({{a, b, c, ip}, program}) do
    # bitwise xor of B and C, stored in B
    debug({a, b, c, ip}, label: "bxc")
    {{a, Bitwise.bxor(b, c), c, ip + 2}, program}
  end

  def out({{a, b, c, ip}, program}) do
    # output the value of the combo operand modulo 8
    debug({a, b, c, ip}, label: "out")

    {
      {a, b, c, ip + 2},
      Map.put(program, :out, [
        combooperand({a, b, c, ip}, program) |> Integer.mod(8) | program[:out]
      ])
    }
  end

  def prog1step({{a, b, c, ip}, program}) do
    case program[ip] do
      0 -> adv({{a, b, c, ip}, program})
      1 -> bxl({{a, b, c, ip}, program})
      2 -> bst({{a, b, c, ip}, program})
      3 -> jnz({{a, b, c, ip}, program})
      4 -> bxc({{a, b, c, ip}, program})
      5 -> out({{a, b, c, ip}, program}) |> checkoutputp2(program[:initialA])
      6 -> bdv({{a, b, c, ip}, program})
      7 -> cdv({{a, b, c, ip}, program})
      nil -> {:halt, {{a, b, c, ip}, program}}
    end
  end

  def checkoutput({state, program}) do
    program[:out]
    |> Enum.reverse()
    |> Enum.join(",")
    |> debug(label: "checkoutput")

    {state, program}
  end

  def checkoutputinfo({state, program}) do
    program[:out]
    |> Enum.reverse()
    |> Enum.join(",")
    |> info(label: "checkoutput")

    {state, program}
  end

  def compare([], []) do
    :match
  end

  def compare([], [_head | _program]) do
    0
  end

  def compare([head_o | output], [head_p | program]) do
    if head_o == head_p do
      case compare(output, program) do
        :match -> :match
        :fail -> :fail
        len -> len + 1
      end
    else
      :fail
    end
  end

  def checkoutputp2({state, program}, initialA) do
    if initialA != nil do
      if Integer.mod(initialA, 10000) == 0 do
        info("Checking output for #{initialA}", label: "checkoutputp2")
      end
    end

    currentout =
      program[:out]
      |> Enum.reverse()

    case compare(currentout, program[:program]) do
      :match ->
        IO.puts("Found a match! #{initialA}")
        IO.puts({state, program})

      :fail ->
        nil

      1 ->
        debug("partial match of length 1", label: "checkoutputp2 #{initialA}")

      2 ->
        debug("partial match of length 2", label: "checkoutputp2 #{initialA}")

      3 ->
        debug("partial match of length 3", label: "checkoutputp2 #{initialA}")

      len ->
        info("partial match of length #{len}", label: "checkoutputp2 #{initialA}")
    end

    {state, program}
  end

  def prog(machine) do
    case prog1step(machine) do
      {:halt, newmachine} -> newmachine
      newmachine -> prog(newmachine)
    end
  end

  def runpart1(input) do
    input
    # |> Task.async_stream(fn line -> {line, todo1(line)} end)
    # |> Enum.map(fn {:ok, result} -> result end)
    # |> Enum.map(fn line -> {line, todo1(line)} end)
    |> debug(label: "run2")
    |> prog()
    |> checkoutput()
  end

  def tothreebitbinary(n) do
    n
    |> debug(label: "tothreebitbinary in")
    |> Integer.to_string(2)
    |> debug(label: "tothreebitbinary binary")
    |> String.pad_leading(3, "0")
    |> debug(label: "tothreebitbinary padded")
    |> String.split("", trim: true)
    |> debug(label: "tothreebitbinary split")
    |> Enum.map(&String.to_integer/1)
    |> debug(label: "tothreebitbinary ints")
  end

  # def matchns(infomap) do
  #   n = infomap["n"]
  #   a_ns =

  # end

  def reverseoutput(out) do
    [o2, o1, o0] = tothreebitbinary(out)

    0..7
    |> Enum.map(fn n -> {n, tothreebitbinary(n)} end)
    |> Enum.map(fn {n, [s2, s1, s0]} ->
      %{
        "n" => n,
        "s0" => s0,
        "s1" => s1,
        "s2" => s2,
        # shift is lowest 3 bits of a, xor 1, i.e. invert a0
        "a0" => 1 - s0,
        "a1" => s1,
        "a2" => s2,
        # n is depending on how much we shift (n+1 bits shifted)
        # a shifted n+1 bits, mod 8 (i.e. lowest 3 bits), xor a mod 8 xor 4 = output
        # and a mod 8 xor 4 = shift xor 5
        # ergo (shift xor 5) xor out
        "a_n" => Bitwise.bxor(o0, 1 - s0),
        "a_n+1" => Bitwise.bxor(o1, s1),
        "a_n+2" => Bitwise.bxor(o2, 1 - s2)
      }
    end)
    |> Enum.map(fn infomap ->
      case infomap["n"] do
        # 0 overlap: 3
        0 -> %{
          "n" => infomap["n"],
          "s0" => infomap["s0"],
          "s1" => infomap["s1"],
          "s2" => infomap["s2"],
          "a0" => if infomap["a0"] == infomap["a_n"] do infomap["a0"] else "X" end,
          "a1" => if infomap["a1"] == infomap["a_n+1"] do infomap["a1"] else "X" end,
          "a2" => if infomap["a2"] == infomap["a_n+2"] do infomap["a2"] else "X" end,
          "a_n" => infomap["a_n"],
          "a_n+1" => infomap["a_n+1"],
          "a_n+2" => infomap["a_n+2"]
        }
        # 1 overlap: 2
        1 -> %{
          "n" => infomap["n"],
          "s0" => infomap["s0"],
          "s1" => infomap["s1"],
          "s2" => infomap["s2"],
          "a0" => infomap["a0"],
          "a1" => if infomap["a1"] == infomap["a_n"] do infomap["a1"] else "X" end,
          "a2" => if infomap["a2"] == infomap["a_n+1"] do infomap["a2"] else "X" end,
          "a3" => infomap["a_n+2"],
          "a_n" => infomap["a_n"],
          "a_n+1" => infomap["a_n+1"],
          "a_n+2" => infomap["a_n+2"]
        }
        # 2 overlap: 1
        2 -> %{
          "n" => infomap["n"],
          "s0" => infomap["s0"],
          "s1" => infomap["s1"],
          "s2" => infomap["s2"],
          "a0" => infomap["a0"],
          "a1" => infomap["a1"],
          "a2" => if infomap["a2"] == infomap["a_n"] do infomap["a2"] else "X" end,
          "a3" => infomap["a_n+1"],
          "a4" => infomap["a_n+2"],
          "a_n" => infomap["a_n"],
          "a_n+1" => infomap["a_n+1"],
          "a_n+2" => infomap["a_n+2"]
        }
        # no overlap
        n -> %{
          "n" => infomap["n"],
          "s0" => infomap["s0"],
          "s1" => infomap["s1"],
          "s2" => infomap["s2"],
          "a0" => infomap["a0"],
          "a1" => infomap["a1"],
          "a2" => infomap["a2"],
          "a#{n}" => infomap["a_n"],
          "a#{n+1}" => infomap["a_n+1"],
          "a#{n+2}" => infomap["a_n+2"],
          "a_n" => infomap["a_n"],
          "a_n+1" => infomap["a_n+1"],
          "a_n+2" => infomap["a_n+2"]
        }
      end
    end)
    |> Enum.map(fn infomap ->
      # Map.put(infomap, "fullA", [
      #   infomap["a10"],
      #   infomap["a9"],
      #   infomap["a8"],
      #   infomap["a7"],
      #   infomap["a6"],
      #   infomap["a5"],
      #   infomap["a4"],
      #   infomap["a3"],
      #   infomap["a2"],
      #   infomap["a1"],
      #   infomap["a0"],
      # ])
      {
        infomap["n"],
        [
          infomap["a9"],
          infomap["a8"],
          infomap["a7"],
          infomap["a6"],
          infomap["a5"],
          infomap["a4"],
          infomap["a3"],
          infomap["a2"],
          infomap["a1"],
          infomap["a0"],
        ]
        |> Enum.map(fn x -> if x == nil do "-" else x end end)
        |> Enum.join("")
      }
    end)
  end

  def programforonepart(a) do
    a_part = Integer.mod(a, 8)

    out =
      Bitwise.bxor(
        Bitwise.bxor(
          a_part,
          4
        ),
        Bitwise.>>>(a, Bitwise.bxor(a_part, 1))
      )
  end

  def runpart2({_state, program}) do
    # the program does cycles of 3 bits of A, so let's start with splitting it

    potentialoutputs =
      program[:program]
      |> info(label: "runpart2")
      |> Enum.map(fn a ->
        programforonepart(a)
      end)

    # 1..10000000
    # # |> Enum.map(fn n -> 2*n+1 end)
    # # |> List.flatten()
    # |> info(label: "runpart2")
    # |> Enum.map(fn a ->
    #   {{a, 0, 0, 0}, Map.put(program, :initialA, a)}
    #   |> debug(label: "run2")
    #   |> prog()
    #   |> checkoutput()
    # end)
  end
end

Puzzleday17.tothreebitbinary(3) |> IO.inspect(pretty: true, label: "tothreebitbinary")

0..7
|> Enum.map(fn n -> Puzzleday17.tothreebitbinary(n) end)
|> IO.inspect(pretty: true, label: "tothreebitbinary")

0..7
|> Enum.map(fn n ->
  Puzzleday17.reverseoutput(n)
  |> IO.inspect(pretty: true, label: "reverseoutput #{n}")
end)

# Puzzleday17.read_input("input/2024/day17inputtest.txt")
# |> Puzzleday17.runpart1()
# |> IO.inspect(pretty: true, label: "testinput, part1")

# Puzzleday17.read_input("input/2024/day17input.txt")
# |> Puzzleday17.runpart1()
# |> IO.inspect(pretty: true, label: "realinput, part1")

# # Puzzleday17.read_input("input/2024/day17inputtest.txt")
# # |> Puzzleday17.runpart2()
# # |> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday17.read_input("input/2024/day17input.txt")
|> Puzzleday17.runpart2()
|> IO.inspect(pretty: true, label: "realinput, part2")
# now a lot of manual shit leads to 164278764924605, idk
