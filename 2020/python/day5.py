def line_int(line):
    line_b = (
        line.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1")
    )
    line_i = int(line_b, 2)
    print(line, line_b, line_i)
    return line_i


line_int("FBFBBFFRLR")

with open("day5input.txt") as infile:
    line_list = sorted(line_int(line) for line in infile)

print("max:", max(line_list))

print(line_list)
last = line_list[0]
for i in line_list[1:]:
    if i != (last + 1):
        print(i, last)
    last = i
