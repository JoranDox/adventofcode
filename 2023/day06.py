import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
with open(aoc_dir.joinpath("input/2023/day06inputtest.txt")) as f:
    # with open(aoc_dir.joinpath("input/2023/day06input.txt")) as f:
    data = f.read().strip()


def boatdistance(timebuttonheld, totalracetime):
    return (totalracetime - timebuttonheld) * timebuttonheld


accum = 1
for time, distance in zip(*[d.split() for d in data.splitlines()]):
    # print(time, distance)
    if time.startswith("Time:"):
        continue  # skip header
    time = int(time)
    distance = int(distance)
    n_better = 0
    for i in range(1, time):
        bd = boatdistance(i, time)
        # print(i, bd)
        if bd > distance:
            n_better += 1
    # print(n_better)
    accum *= n_better
print("p1:", accum)

with open(aoc_dir.joinpath("input/2023/day06inputp2.txt")) as f:
    data = f.read().strip()
time, distance = data.splitlines()
# time, distance = 71530, 940200
time = int(time)
distance = int(distance)
print(time, distance)


# binary search didn't matter because naive worked :cry:
def bsearch(amin_orig=1, amax_orig=time, tobeat=distance, fun=boatdistance):
    amin = amin_orig
    amax = amax_orig
    vmin = fun(amin, amax_orig)
    vmax = fun(amax, amax_orig)
    while amax - amin > 1:  # gap is bigger
        attempt = amax / 2 + amin
        result = ...


for i in range(1, time):
    bd = boatdistance(i, time)
    # print(i, bd)
    if bd > distance:
        firsti = i
        print("firsti =", firsti)
        break

for i in range(time, 0, -1):
    bd = boatdistance(i, time)
    # print(i, bd)
    if bd > distance:
        lasti = i
        print("lasti =", lasti)
        break
print(lasti - firsti + 1)
