
import pathlib
aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent

###
test = False
###

if test:
    with open(aoc_dir.joinpath("input/2025/day08inputtest.txt")) as f:
        data = f.read().strip()
    num_connections = 10
else:
    with open(aoc_dir.joinpath("input/2025/day08input.txt")) as f:
        data = f.read().strip()
    num_connections = 1000

boxloc = tuple[int,int,int]
boxlocs: list[boxloc] = []
for line in data.splitlines():
    x,y,z = map(int, line.split(","))
    boxlocs.append((x,y,z))

def euclidean_proxy(a: boxloc, b: boxloc) -> int:
    # don't bother taking sqrt, we just need to compare them
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

assert len(boxlocs) == 20 or len(boxlocs) == 1000
box_dists: dict[tuple[boxloc, boxloc], int] = {}
for box1 in boxlocs:
    for box2 in boxlocs:
        if box1 == box2:
            # print("skipping", box1, box2)
            continue # skip self
        if box1 > box2:
            b1, b2 = box2, box1
        else:
            b1, b2 = box1, box2
        if (b1, b2) in box_dists:
            # print("already have", box1, box2)
            continue # already computed
        # print("computing", b1, b2)
        box_dists[(b1, b2)] = euclidean_proxy(b1, b2)

# print(len(box_dists))
# print(expected)
ordered_locs = sorted([(dist, box, nearest) for (box, nearest), dist in box_dists.items()])
# print(ordered_locs)
cirquits = [set((loc,)) for loc in boxlocs] # all individual cirquits to start

successful_connections = 0
while successful_connections < num_connections:
    dist, box, nearest = ordered_locs.pop(0)
    boxc = None
    nearestc = None
    for c in cirquits:
        if box in c:
            boxc = c
        if nearest in c:
            nearestc = c
    assert boxc is not None
    assert nearestc is not None
    # if boxc == nearestc:
    #     # print("skipping same cirquit", box, nearest, boxc)
    #     continue

    newcirquits = [
        c for c in cirquits if c != boxc and c != nearestc
    ] + [boxc | nearestc]
    # print("joining", box, nearest)
    successful_connections += 1
    # print("successful connections:", successful_connections, " | cirquit sizes:", [len(c) for c in newcirquits])
    cirquits = newcirquits

top = sorted([len(c) for c in cirquits])
print("All cirquit sizes:", top)
top3 = top[:-4:-1]
print("Top 3 cirquits sizes:", top3)
print("multiplied:", top3[0] * top3[1] * top3[2])

while len(cirquits) > 1: # lazy copy for part 2
    dist, box, nearest = ordered_locs.pop(0)
    boxc = None
    nearestc = None
    for c in cirquits:
        if box in c:
            boxc = c
        if nearest in c:
            nearestc = c
    assert boxc is not None
    assert nearestc is not None
    # if boxc == nearestc:
    #     # print("skipping same cirquit", box, nearest, boxc)
    #     continue

    newcirquits = [
        c for c in cirquits if c != boxc and c != nearestc
    ] + [boxc | nearestc]
    # print("joining", box, nearest)
    successful_connections += 1
    # print("successful connections:", successful_connections, " | cirquit sizes:", [len(c) for c in newcirquits])
    cirquits = newcirquits

print("last 2 boxes joined:", box, nearest)
result = box[0] * nearest[0]
print(result)
