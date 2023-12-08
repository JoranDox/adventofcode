import string

# with open("day12inputtest.txt") as f:
with open("day12input.txt") as f:
    data = f.read().strip()

upper = string.ascii_uppercase
lower = string.ascii_lowercase


print(data)

paths = {}
for line in data.splitlines():
    i, j = line.split("-")
    if i not in paths:
        paths[i] = [j]
    else:
        paths[i].append(j)
    if j not in paths:
        paths[j] = [i]
    else:
        paths[j].append(i)


print(paths)

final = set()
checked = set()
tocheck = {(("start",), False)}
while tocheck:
    p, visitedtwice = tocheck.pop()
    checked |= {p}
    # print(p, paths[p[-1]])
    for path in paths[p[-1]]:
        visitedtwice2 = visitedtwice
        # print(path)
        if path == "start":
            continue
        if path.islower() and path in p:
            if visitedtwice:
                continue
            else:
                visitedtwice2 = True
        p2 = p + (path,)
        if p2 in checked:
            continue
        if path == "end":
            final |= {p2}
            # print("finished path:",p2)
            continue

        tocheck |= {(p2, visitedtwice2)}
# [print(f) for f in final]
print(len(final))

# start,A,b,A,c,A,end
# start,A,b,A,end
# start,A,b,end
# start,A,c,A,b,A,end
# start,A,c,A,b,end
# start,A,c,A,end
# start,A,end
# start,b,A,c,A,end
# start,b,A,end
# start,b,end
# finished path: ('start', 'A', 'c', 'b', 'end')
# finished path: ('start', 'A', 'c', 'b', 'A', 'd', 'end')
# finished path: ('start', 'A', 'c', 'b', 'A', 'end')
# finished path: ('start', 'A', 'b', 'A', 'd', 'end')
# finished path: ('start', 'A', 'c', 'A', 'b', 'end')
# finished path: ('start', 'A', 'b', 'A', 'c', 'end')
# finished path: ('start', 'A', 'c', 'A', 'b', 'A', 'd', 'end')
# finished path: ('start', 'A', 'c', 'A', 'b', 'A', 'end')
# finished path: ('start', 'A', 'b', 'A', 'c', 'A', 'end')
