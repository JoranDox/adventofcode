import pathlib

aoc_dir = pathlib.Path(__file__).resolve().absolute().parent.parent
with open(aoc_dir.joinpath("input/2025/day11inputtest.txt")) as f:
    # with open(aoc_dir.joinpath("input/2025/day11input.txt")) as f:
    data = f.read().strip()

nodes: dict[str, list[str]] = {}
for line in data.splitlines():
    # for line in data.split("\n\n"):
    source, *destinations = line.split()
    assert source.endswith(":")
    source = source[:-1]
    nodes[source] = destinations


tocheck = [("you", 1)]
outcount = 0
while tocheck:
    current, paths = tocheck.pop()
    for dest in nodes[current]:
        if dest == "out":
            outcount += paths
        else:
            tocheck.append((dest, paths))
print(outcount)


# part2

# with open(aoc_dir.joinpath("input/2025/day11inputtest2.txt")) as f:
with open(aoc_dir.joinpath("input/2025/day11input.txt")) as f:
    data = f.read().strip()

nodes: dict[str, list[str]] = {}
for line in data.splitlines():
    # for line in data.split("\n\n"):
    source, *destinations = line.split()
    assert source.endswith(":")
    source = source[:-1]
    nodes[source] = destinations


def simplify_nodes(nodes: dict[str, list[str]]) -> dict[str, list[str]]:
    newnodes: dict[str, list[str]] = {}
    replacements: dict[str, str] = {}
    deletions: set[str] = set()
    never_delete: set[str] = {"svr", "dac", "fft", "out"}
    changes = False
    print("starting simplification with", len(nodes), "nodes")
    print("nodes:",nodes)
    for src, dests in nodes.items():
        if src in never_delete:
            continue
        if len(dests) == 1:
            dest = dests[0]
            if dest in never_delete:
                continue
            if dest == src:
                deletions.add(src)
            else:
                replacements[src] = dest  # skip nodes with single destination
            changes = True

    print("rep:", replacements)
    print("del:", deletions)

    print("found", len(replacements), "nodes to replace")
    if changes:
        for src, dests in nodes.items():
            if src in replacements:
                continue  # this node is being removed
            newdests: list[str] = []
            for dest in dests:
                if dest in deletions:
                    continue
                while dest in replacements:
                    dest = replacements[dest]
                newdests.append(dest)

            newnodes[src] = newdests
        print("applied replacements, now have", len(newnodes), "nodes")
        return simplify_nodes(newnodes)
    else:
        print(f"removed {len(nodes) - len(newnodes)} nodes by simplification")
        return nodes


print(len(nodes), "nodes before simplification")
nodes = simplify_nodes(nodes)
print(len(nodes), "nodes after simplification")
print(nodes)
reversenodes: dict[str, list[str]] = {}
for src, dests in nodes.items():
    for dest in dests:
        reversenodes.setdefault(dest, []).append(src)


def downstream_from(target: str, nodes: dict[str, list[str]] = nodes) -> set[str]:
    result = {target}
    tocheck = [target]
    while tocheck:
        current = tocheck.pop()
        for dest in nodes.get(current, []):
            if dest not in result:
                result.add(dest)
                tocheck.append(dest)
    return result


def upstream_from(target: str):
    return downstream_from(target, reversenodes)


useful_downstream = {"out"}
tocheck = list(useful_downstream)
while tocheck:
    current = tocheck.pop()
    if current == "out":
        continue
    for dest in nodes[current]:
        if dest not in useful_downstream:
            useful_downstream.add(dest)
            tocheck.append(dest)

useful_upstream = {"dac", "fft"}
tocheck = list(useful_upstream)
while tocheck:
    current = tocheck.pop()
    if current == "svr":
        continue
    for src in reversenodes[current]:
        if src not in useful_upstream:
            useful_upstream.add(src)
            tocheck.append(src)
assert "svr" in useful_upstream
assert "out" in useful_downstream
print("ok")
print(len(useful_upstream))

# so useful nodes are
# downstream from svr
# upstream or downstream from dac
# upstream or downstream from fft
# upstream from out
# any node that doesn't meet those criteria can be deleted entirely

first, second = "dac", "fft"
if "fft" in downstream_from("dac"):
    print("fft downstream of dac")
    assert not "dac" in downstream_from("fft")

if "dac" in downstream_from("fft"):
    print("dac downstream of fft")
    assert not "fft" in downstream_from("dac")
    first, second = "fft", "dac"

order = ["svr", first, second, "out"]

useful_nodes = {"svr", "dac", "fft", "out"} | (
    downstream_from("svr") & upstream_from(first)
    | downstream_from(first) & upstream_from(second)
    | downstream_from(second) & upstream_from("out")
)
print(len(useful_nodes))
partnodes = {
    "svr": downstream_from("svr") & upstream_from(first),
    first: downstream_from(first) & upstream_from(second),
    second: downstream_from(second) & upstream_from("out"),
}
targetnode = {
    "svr": first,
    first: second,
    second: "out",
}


# partnodes = {part: nodeset & set(nodes) for part, nodeset in partnodes.items()}


print("partnodes sizes:", {k: len(v) for k, v in partnodes.items()})
outcount = 0
seenpaths: set[set[str]] = set()
tocheck = [("svr", 1, {"svr"})]
nexttocheck = []


def countpathsfrom(source: str, destination: str, allowed: set[str]) -> int:
    tocheck = [(source, 1)]
    pathcount = 0
    while tocheck:
        current, paths = tocheck.pop()
        for dest in nodes[current]:
            if dest == destination:
                pathcount += paths
            elif dest in allowed:
                tocheck.append((dest, paths))
    return pathcount

p1 = countpathsfrom("svr", first, partnodes["svr"])
print("p1", p1)
p2 = countpathsfrom(first, second, partnodes[first])
print("p2", p2)
p3 = countpathsfrom(second, "out", partnodes[second])
print("p3", p3)
print("final", p1*p2*p3)

# for part, target in targetnode.items():
#     print("part", part, "target", target, "nodes", len(partnodes[part]))
#     while tocheck:
#         # print(len(tocheck))
#         current, paths, seenset = tocheck.pop()
#         for dest in nodes[current]:
#             if dest == target:
#                 if dest == "out":
#                     print("found paths:", paths, outcount, sorted(seenset))
#                     outcount += paths
#                 else:
#                     nexttocheck.append((dest, paths, seenset | {dest}))
#                 continue

#             if dest not in partnodes[part]:
#                 continue  # invalid path order

#             if dest in seenset:
#                 # loop detected
#                 continue

#             if dest == second and first not in seenset:
#                 # can't reach second before first
#                 continue

#             tocheck.append((dest, paths, seenset | {dest}))
# print(outcount)
