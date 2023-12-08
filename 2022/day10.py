import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
# with open(aoc_dir.joinpath("input/2022/day10inputtest.txt")) as f:
with open(aoc_dir.joinpath("input/2022/day10input.txt")) as f:
    data = f.read().strip()

x = 1
splitdata = data.splitlines()
queue = []
accum = 0
crt = []

for line in splitdata:
    if line == "noop":
        queue.append(0)
    else:
        _, val = line.split()
        queue.append(0)
        queue.append(int(val))

# print(queue)

for c, val in enumerate(queue):
    if ((c % 40) - x) in (-1, 0, 1):
        crt.append("█")
    else:
        crt.append(" ")

    x += val
    cyclenum = c + 2
    if not ((cyclenum - 20) % 40):
        # print(cyclenum, "    ", x)
        accum += (cyclenum) * x

    # print(cyclenum, val, x, )

print("p1:", accum)

print("p2:")
print("." * 42)
print("." + "".join(crt[:40]) + ".")
print("." + "".join(crt[40:80]) + ".")
print("." + "".join(crt[80:120]) + ".")
print("." + "".join(crt[120:160]) + ".")
print("." + "".join(crt[160:200]) + ".")
print("." + "".join(crt[200:240]) + ".")
print("." * 42)
# not FFC7FIH5
# not FECZELH6
# not FECZELHG
# FECZELHE


# while c < len(splitdata) or any([c <= i for i in cycles]):
#     try:
#         line = splitdata[c]
#     except:
#         # out of data
#         line = "noop"
#         pass

#     # if int(c) in cycles:
#     #     x += cycles[int(c)]

#     if line == "noop":
#         pass
#     else:
#         _, val = line.split()
#         # cycles[int(c)+2] = int(val)
#         x += int(val)
#         actual_cycle_count += 1
#     print(x)
#     if  not((actual_cycle_count -20 )% 40):
#         print("    ", x)
#     actual_cycle_count += 1
#     c += 1
