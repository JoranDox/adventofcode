


defmodule Puzzleday13 do
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

    defmodule Point2d do
        defstruct [:x, :y]
    end

    def point2dsum(p1, p2) do
        %Point2d{x: p1.x + p2.x, y: p1.y + p2.y}
    end

    def point2dmul(p, n) do
        %Point2d{x: p.x * n, y: p.y * n}
    end

    defmodule ClawMachine do
        defstruct [:button_a, :button_b, :prize]
    end

    def read_input(filename, add \\ 0) do
        regex = ~r/Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)/
        # regex = ~r/Button A: X+(\d+)/
                #   "Button A: X+26,    Y+66   \nButton B: X+67   , Y+21   \nPrize: X=12748, Y=12176"
        File.read!(filename)
        |> String.split("\n\n", trim: true)
        # these are the claw machines
        |> debug(label: "read_input 1")
        |> Enum.map(fn clawmachine ->
            debug(clawmachine, label: "clawmachine")
            Regex.scan(regex, clawmachine)
            |> debug(label: "scan")
            |> hd() # only one match
            |> tl() # remove the first match, which is the whole match
            |> debug(label: "scan nums")
            |> then(fn [a_x, a_y, b_x, b_y, p_x, p_y] ->
                debug([a_x, a_y, b_x, b_y, p_x, p_y], label: "scan nums as integers")
                %ClawMachine{
                    button_a: %Point2d{x: String.to_integer(a_x), y: String.to_integer(a_y)},
                    button_b: %Point2d{x: String.to_integer(b_x), y: String.to_integer(b_y)},
                    prize: %Point2d{x: String.to_integer(p_x)+add, y: String.to_integer(p_y)+add}
                }
            end)
            |> debug(label: "clawmachine 2")

        end)
        |> debug(label: "read_input 2")
    end


    # def dynamicprogramming(clawmachine) do
    #     dynamicprogramming(clawmachine, 0, 0, %{})
    # end

    def cost({numAs, numBs}) do
        3*numAs + numBs
    end


    # def dynamicprogramming(clawmachine, numAs, numBs, [head | todo]) do
    #     mycost = cost({numAs,numBs})
    #     point = point2dsum(point2dmul(clawmachine.button_a, numAs),point2dmul(clawmachine.button_b, numBs))
    #     debug({numAs, numBs, mycost, point, clawmachine.prize}, label: "dynamicprogramming in")
    #     case point do
    #         # this is the best solution
    #         point when point == clawmachine.prize -> {numAs, numBs, mycost} |> debug(label: "dynamicprogramming win")
    #         # this is not a solution
    #         point when point.x > clawmachine.prize.x or point.y > clawmachine.prize.y -> nil |> debug(label: "dynamicprogramming overshoot")
    #         # this is not a solution
    #         point -> case seen[point] do
    #             # we've already been more efficiently
    #             pcost when pcost < mycost -> nil |> debug(label: "dynamicprogramming seen")
    #             # new point or we're better, do stuff
    #             _ -> case {
    #                 dynamicprogramming(clawmachine, numAs+1, numBs, Map.put(seen, point, mycost)),
    #                 dynamicprogramming(clawmachine, numAs, numBs+1, Map.put(seen, point, mycost)) # todo: share the seen?
    #             } |> debug(label: "subtasks") do
    #                 {nil, nil} -> nil |> debug(label: "dynamicprogramming deadend")
    #                 {nil, {a,b,c}} -> {a,b,c} |> debug(label: "dynamicprogramming A increase deadend")
    #                 {{a,b,c}, nil} -> {a,b,c} |> debug(label: "dynamicprogramming B increase deadend")
    #                 {{a,b,c}, {_d,_e,f}} when c < f -> {a,b,c} |> debug(label: "dynamicprogramming A increase better")
    #                 {{_a,_b,_c}, {d,e,f}} -> {d,e,f} |> debug(label: "dynamicprogramming B increase better")
    #             end
    #         end
    #     end
    #     |> debug(label: "dynamicprogramming out")
    # end

    def part1math(c) do
        {c,
            {
                (
                    (
                        (c.prize.y/c.button_b.y) - (c.prize.x/c.button_b.x)
                    ) / (
                        (c.button_a.y/c.button_b.y) - (c.button_a.x/c.button_b.x)
                    )
                ),
                (
                    (
                        (c.prize.y/c.button_a.y) - (c.prize.x/c.button_a.x)
                    ) / (
                        (c.button_b.y/c.button_a.y) - (c.button_b.x/c.button_a.x)
                    )
                )
            }
        }
    end

    def targethit?(clawmachine, {numAs, numBs}) do
        clawmachine.prize == point2dsum(
            point2dmul(clawmachine.button_a, numAs),
            point2dmul(clawmachine.button_b, numBs)
        )
    end

    def score(clawmachine, numAs, numBs) do
        if targethit?(clawmachine, {numAs, numBs}) do
            cost({numAs, numBs})
        else
            0
        end
    end

    def runpart1(input) do
        input
        |> debug(label: "run0")
        |> Enum.map(fn clawmachine -> part1math(clawmachine) end)
        |> debug(label: "run2")
        |> Enum.map(fn {c, {as, bs}} -> score(c, round(as), round(bs)) end)
        |> debug(label: "run3")
        |> Enum.sum()
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        # |> Enum.map(fn line -> {line, todo1(line)} end)
        # |> debug(label: "run2")
        # |> Enum.count(fn {_line, sl} -> sl end)
        # |> debug(label: "run3")
    end

    def runpart2(input) do
        input
        # |> Enum.map(fn line -> {line, todo2(line)} end)
        # |> debug(label: "run2")
        # |> Enum.count(fn {_line, sl} -> sl end)
        # |> debug(label: "run3")
    end
end

Puzzleday13.read_input("input/2024/day13inputtest.txt")
|> Puzzleday13.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzleday13.read_input("input/2024/day13input.txt")
|> Puzzleday13.runpart1()
|> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday13.read_input("input/2024/day13inputtest.txt", 10000000000000)
|> Puzzleday13.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part2")

Puzzleday13.read_input("input/2024/day13input.txt", 10000000000000)
|> Puzzleday13.runpart1()
|> IO.inspect(pretty: true, label: "realinput, part2")
