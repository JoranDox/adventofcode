defmodule Part1 do
  def run do
    # File.read!("input/2024/day01inputtest.txt")
    File.read!("input/2024/day01input.txt")
    |> String.split("\n")
    # |> IO.inspect(pretty: true)
    |> Enum.map(fn line -> String.split(line) end)
    # |> IO.inspect(pretty: true)
    |> Enum.map(fn line -> Enum.map(line, &String.to_integer/1) end)
    # |> IO.inspect(pretty: true)
    # transpose
    |> Enum.zip()
    |> Enum.map(&Tuple.to_list/1)
    # |> IO.inspect(pretty: true)
    |> Enum.map(fn line -> Enum.sort(line) end)
    # |> IO.inspect(pretty: true)
    |> Enum.zip()
    |> Enum.map(&Tuple.to_list/1)
    # |> IO.inspect(pretty: true)
    |> Enum.map(fn [a,b] -> abs(a-b) end)
    # |> IO.inspect(pretty: true)
    |> Enum.sum()
    |> IO.inspect(pretty: true)
  end
end

defmodule Part2 do
  def process(c1, col2) do
      Enum.count(col2, fn c2 -> c1 == c2 end) * c1
  end

  def run do
      # File.read!("input/2024/day01inputtest.txt")
      File.read!("input/2024/day01input.txt")
      |> String.split("\n")
      |> IO.inspect(pretty: true)
      |> Enum.map(fn line -> String.split(line) end)
      |> IO.inspect(pretty: true)
      |> Enum.map(fn line -> Enum.map(line, &String.to_integer/1) end)
      |> IO.inspect(pretty: true)
      # transpose
      |> Enum.zip()
      |> Enum.map(&Tuple.to_list/1)
      |> IO.inspect(pretty: true)
      |> then(fn [col1, col2] ->
        col1
        |> Task.async_stream(fn c1 -> process(c1, col2) end)
        |> Enum.map(fn {:ok, result} -> result end)
      end)
      |> IO.inspect(pretty: true)
      |> Enum.sum()
      |> IO.inspect(pretty: true)
  end
end

Part2.run()
