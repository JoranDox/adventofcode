
# with open("day09inputtest.txt") as f:
with open("day09input.txt") as f:
    data = f.readlines()

data2 = [list(map(int,d.strip())) for d in data]
# print(data2)
totals = 0
largest = []
for i, line in enumerate(data2):
    for j, val in enumerate(line):
        smaller = 0
        # print(i,j,val)
        for i2 in -1, 0, +1:
            for j2 in -1, 0, +1:
                if abs(i2) + abs(j2) == 1:
                    try:
                        # print("checking", i+i2, j+j2, data2[i + i2][j + j2])
                        if val >= data2[i + i2][j + j2]:
                            smaller += 1
                    except:
                        pass
        if smaller == 0:
            # print("found", i,j, val)
            totals += val + 1

            # now find the bassin
            bassin = set()
            checked = set()
            tocheck = [(val,i,j)]
            while tocheck:
                valcheck, icheck, jcheck = tocheck.pop()
                if (icheck,jcheck) in checked:
                    continue
                checked |= {(icheck,jcheck),}

                for i2 in -1, 0, +1:
                    for j2 in -1, 0, +1:
                        if (abs(i2) + abs(j2) == 1) and icheck+i2>=0 and jcheck+j2 >= 0:
                            try:
                                newval = data2[icheck + i2][jcheck + j2]
                                if newval < 9:
                                    print("adding",icheck + i2, jcheck + j2, newval)
                                    bassin |= {(icheck + i2, jcheck + j2),}
                                    tocheck.append((newval,icheck+i2,jcheck+j2))
                            except:
                                pass
            print("checked", i,j, bassin, len(bassin))
            print(checked)


            largest.append((len(bassin),(i,j)))

# part1
print(totals)
# part2
print(sorted(largest)[-3:])
m = 1
for v,_ in sorted(largest)[-3:]:
    m *= v
print(m)