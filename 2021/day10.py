
# with open("day10inputtest.txt") as f:
with open("day10input.txt") as f:
    data = f.readlines()

mapbrackets = {
    "{": "}",
    "(": ")",
    "<": ">",
    "[": "]",
}

points = {
    ")": 3, # points.
    "]": 57, # points.
    '}': 1197, # points.
    ">": 25137, # points.
}
# part 1

total = 0
for line in data:
    stack = []
    for c in line.strip():
        if c in mapbrackets:
            stack.append(c)
        else:
            c2 = stack.pop()
            if mapbrackets[c2] != c:
                total += points[c]
                break

print(total)

points2 = {
    ")": 1, # point.
    "]": 2, # points.
    "}": 3, # points.
    ">": 4, # points.
}

# part 2
linescores = []
for line in data:
    stack = []
    goodline = True
    for c in line.strip():
        if c in mapbrackets:
            stack.append(c)
        else:
            c2 = stack.pop()
            if mapbrackets[c2] != c:
                goodline = False
                break
    if goodline:
        # print(stack)
        linescore = 0
        while stack:
            linescore *= 5
            linescore += points2[mapbrackets[stack.pop()]]
        # print(linescore)
        linescores.append(linescore)
# print(sorted(linescores))
print(sorted(linescores)[len(linescores) // 2])