
# with open("day13inputtest.txt") as f:
with open("day13input.txt") as f:
    data = f.read().strip()


dots, fold = data.split("\n\n")

dots = {
    tuple([int(t) for t in d.split(",")]) for d in dots.splitlines()
}
# print(dots)
# print(fold)

def hmirror(x,y, xmirror):
    return ((2*xmirror)-x,y) if (x > xmirror) else (x,y)
def vmirror(x,y, ymirror):
    return (x, (2*ymirror)-y) if (y > ymirror) else (x,y)

def printdots(dots):
    printdata = [
        [
            ' ' for _ in range(max([i for i,_ in dots])+1) # max x
        ] for _ in range(max([i for _,i in dots])+1) # max y
    ]

    for i,j in dots:
        printdata[j][i] = '█'

    print("\n".join([''.join(p) for p in printdata]))

firstpart = True
for line in fold.splitlines():
    if not line:
        break
    d,n = line.split("fold along ")[1].split("=")
    if d == "y":
        dots = {vmirror(*dot,int(n)) for dot in dots}
    if d == "x":
        dots = {hmirror(*dot,int(n)) for dot in dots}
    if firstpart:
        print("part 1:", len(dots))
        firstpart = False
    # print(line)
    # printdots(dots)

print('part 2:')
printdots(dots)