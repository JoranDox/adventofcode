


defmodule Puzzleday14 do
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
        read_input("input/2024/day14inputtest.txt")
    end

    def realinput do
        read_input("input/2024/day14input.txt")
    end

    defmodule Robot do
        defstruct [:p, :v]
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

    def point2dmod(p, mod) do
        %Point2d{x: Integer.mod(p.x, mod.x), y: Integer.mod(p.y, mod.y)}
    end

    def move(robot, steps, mod) do
        %Robot{
            p: point2dmod(point2dsum(robot.p, point2dmul(robot.v, steps)), mod),
            v: robot.v
        }
    end

    def read_input(filename) do
        File.read!(filename)
        |> String.split("\n", trim: true)
        |> debug(label: "read_input 1")
        |> Enum.map(fn robot ->
            # p=27,12 v=23,-14
            regex = ~r/p=(\d+),(\d+) v=(-?\d+),(-?\d+)/
            Regex.scan(regex, robot)
            |> debug(label: "scan")
            |> hd() # only one match
            |> tl() # remove the first match, which is the whole match
        end)
        |> debug(label: "read_input 2")
        |> Enum.map(fn [px, py, vx, vy] ->
            %Robot{
                p: %Point2d{x: String.to_integer(px), y: String.to_integer(py)},
                v: %Point2d{x: String.to_integer(vx), y: String.to_integer(vy)}
            }
        end)
        |> debug(label: "read_input 3")
    end

    def maxxy([]), do: {0, 0}
    def maxxy([robot | robots]) do
        {maxx, maxy} = maxxy(robots)
        {max(maxx, robot.p.x), max(maxy, robot.p.y)}
    end

    def visualize(robots, n \\ 0) do
        {maxx, maxy} = maxxy(robots)
        |> debug(label: "maxes")

        Enum.map(0..maxy, fn y ->
            Enum.reduce(0..maxx, "", fn x, acc ->
                case Enum.count(robots, fn robot -> robot.p == %Point2d{x: x, y: y} end) do
                    0 -> acc <> "."
                    num -> acc <> "#{num}"
                end
            end)
            |> debug(label: "vis #{n}")
        end)
        robots
    end

    def quadrants(maxx, maxy) do
        halfx = div(maxx, 2)
        halfy = div(maxy, 2)
        [
            {{0, halfx-1},{0, halfy-1}},
            {{halfx+1, maxx},{0, halfy-1}},
            {{0, halfx-1},{halfy+1, maxy}},
            {{halfx+1, maxx},{halfy+1, maxy}}
        ]
        |> debug(label: "quadrants")
    end

    def robotinquadrant?(robot, quadrant) do
        {{q1x1, q1x2},{q1y1, q1y2}} = quadrant
        q1x1 <= robot.p.x and robot.p.x <= q1x2 and q1y1 <= robot.p.y and robot.p.y <= q1y2
    end

    def score(robots, {maxx, maxy}) do
        quadrants(maxx, maxy)
        |> Enum.map(fn quadrant ->
            robots
            |> Enum.filter(fn robot -> robotinquadrant?(robot, quadrant) end)
            |> visualize()
            |> Enum.count()
            |> debug(label: "q score count")
        end)
        |> Enum.reduce(1, &*/2)
        |> debug(label: "score total")
    end

    def maybechristmastree(robots, {maxx, maxy}) do
        quadrants(maxx, maxy)
        |> Enum.map(fn quadrant ->
            robots
            |> Enum.filter(fn robot -> robotinquadrant?(robot, quadrant) end)
            |> visualize()
            |> Enum.count()
            |> debug(label: "q score count")
        end)
        |> Enum.max()
        |> debug(label: "score max")
    end

    def runpart1(robots, steps \\ 100) do
        robots
        |> debug(label: "run0")

        {maxx, maxy} = maxxy(robots)
        |> debug(label: "maxes")

        mod = %Point2d{x: maxx+1, y: maxy+1}
        |> debug(label: "mod")

        robots
        |> Enum.map(fn robot -> move(robot, steps, mod) end)
        |> visualize()
        # |> Task.async_stream(fn line -> {line, todo1(line)} end)
        # |> Enum.map(fn {:ok, result} -> result end)
        # |> Enum.map(fn line -> {line, todo1(line)} end)
        |> debug(label: "run2")
        |> score({maxx+1, maxy+1})
        # |> Enum.count(fn {_line, sl} -> sl end)
        |> debug(label: "run3")
    end

    def move1andprint(robots, mod, n \\ 0) do
        robots
        |> Enum.map(fn robot -> move(robot, 1, mod) end)
        |> visualize(n)
        |> move1andprint(mod, n+1)
    end

    def runpart2(robots, steps) do
        robots
        |> debug(label: "run0")

        {maxx, maxy} = maxxy(robots)
        |> debug(label: "maxes")

        mod = %Point2d{x: maxx+1, y: maxy+1}
        |> debug(label: "mod")

        robots
        |> Enum.map(fn robot -> move(robot, steps, mod) end)
        |> visualize()
    end

    def preppart2(robots) do
        robots
        |> debug(label: "run0")

        {maxx, maxy} = maxxy(robots)
        |> debug(label: "maxes")

        mod = %Point2d{x: maxx+1, y: maxy+1}
        |> debug(label: "mod")


        robots
        |> move1andprint(mod)
    end
end

Puzzleday14.testinput()
|> Puzzleday14.runpart1()
|> IO.inspect(pretty: true, label: "testinput, part1")

Puzzleday14.realinput()
|> Puzzleday14.runpart1()
|> IO.inspect(pretty: true, label: "realinput, part1")

Puzzleday14.realinput()
|> Puzzleday14.runpart2(7083)
|> IO.inspect(pretty: true, label: "realinput, part2")

# vert line: 12, 113 -> 101 diff
# hor line: 78, 181 -> 103 diff
